
import HitchhikerSource_pb2
import os
import shutil


""" All data will be stored in a dedicated folder that is separate from our codes. """
data_room = "data"


""" We maintain a static folder for the source; this should be revisited where different server services are required. """
server_source = "pilot04"


""" The source base here is static and should be revisited if the data source needs to be dynamic. """
sourse_base = os.path.join("data", "pilot04")


""" static variables for the base, source, and destination folders. """
DATA_BASE = os.path.join(os.path.dirname(__file__), sourse_base)
DATA_SOURCE = os.path.join(DATA_BASE, "source")
DATA_DESTINATION = os.path.join(DATA_BASE, "destination")

def extract_file_content(file_id, client_id):
    """ Load the file data from client source folder to get the file blob """

    DATA_SOURCE_PATH = os.path.join(DATA_SOURCE, client_id)
    file_id = os.path.join(DATA_SOURCE_PATH, file_id)
    file_name, file_extension = os.path.splitext(file_id)
    file_name = os.path.basename(file_name + file_extension)
    with open(file_id, 'rb') as f:
        file_data = f.read()
    file_id = file_id.replace(DATA_SOURCE_PATH+ "/", "")
    file = HitchhikerSource_pb2.File(file_id=file_id, file_name=file_name,
                                        file_type=file_extension, file_blob=file_data)
    return file
    
def file_is_delivered(file_id, destination_id):
    """ checks if file exist in destintion folder """

    DATA_DESTINATION_PATH = os.path.join(DATA_DESTINATION, destination_id)
    file_destination = os.path.join(DATA_DESTINATION_PATH, file_id)
    return os.path.exists(file_destination)

def remove_sourse_file(file_id, client_id):
    """ delete the file from source folder """

    DATA_SOURCE_PATH = os.path.join(DATA_SOURCE, client_id)
    file_source = os.path.join(DATA_SOURCE_PATH, file_id)
    exists = os.path.exists(file_source)
    if exists is True:
        os.remove(file_source)

def process_downloads(client_id):
    """ Get a list of files that exist in the client source folder, including subdirectories. """
    available_files = []
    DATA_SOURCE_PATH = os.path.join(DATA_SOURCE, client_id)
    exists = os.path.exists(DATA_SOURCE_PATH)
    if exists is False:
        return available_files
    for root, directories, files in os.walk(DATA_SOURCE_PATH):
        for file in files:
            file_id = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file_id)
            file_name = os.path.basename(file_name + file_extension)
            file_id = file_id.replace(DATA_SOURCE_PATH+ "/", "")  # Ensure you do not send the full file path back to the client for security reasons.
            available_files.append(HitchhikerSource_pb2.FileList(file_id=file_id, file_name=file_name, file_type=file_extension))
    return available_files

def attempt_to_deliver_to_destivation(available_files, client_id, destination_id):
    """ Attempt to move the file from the client source folder to the destination folder. """
    count = 0
    if  create_destination_directory(destination_id) is True:
        for file in available_files:
            file_path = file.file_id
            directory_path = os.path.dirname(file_path)
            if create_sub_files_destination_directory(directory_path, destination_id) is True:
                if move_file_to_destination(file_path, client_id, destination_id) is True:
                    count = count + 1
    return count

def create_destination_directory(destination_id):
    """ Create the base directory of the destination folder. """
    data_directory = True
    DATA_DESTINATION_PATH = os.path.join(DATA_DESTINATION, destination_id)
    exists = os.path.exists(DATA_DESTINATION_PATH)
    if exists is False:
        try:
           os.mkdir(DATA_DESTINATION_PATH)
        except OSError:
            data_directory = False
    return data_directory

def create_sub_files_destination_directory(directory_path, destination_id):
    """ Create the subdirectories of the destination folder while maintaining the folder structure. """
    data_directory = True
    DATA_DESTINATION_PATH = os.path.join(DATA_DESTINATION, destination_id)
    if directory_path:
        exists = os.path.exists(os.path.join(DATA_DESTINATION_PATH, directory_path))
        if exists is False:
            try:
                os.mkdir(os.path.join(DATA_DESTINATION_PATH, directory_path))
            except OSError:
                data_directory = False
    return data_directory

def move_file_to_destination(file_path, client_id, destination_id):
    """ Move the file from the source folder to the destination folder. """
    DATA_SOURCE_PATH = os.path.join(DATA_SOURCE, client_id)
    DATA_DESTINATION_PATH = os.path.join(DATA_DESTINATION, destination_id)
    file_source = os.path.join(DATA_SOURCE_PATH, file_path)
    file_destination = os.path.join(DATA_DESTINATION_PATH, file_path)
    exists = os.path.exists(file_destination)
    if exists is False:
        shutil.copyfile(file_source, file_destination)
    return not exists
    
def get_downloads(client_id, destination_id):
    """ get downloads while moving files to their destination. """
    available_files = process_downloads(client_id)
    attempt_to_deliver_to_destivation(available_files, client_id, destination_id)
    return available_files

def get_file_size(file_path):
    try:
        file_size = os.path.getsize(file_path)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print(f"File does not exist: {file_path}")
            file_size = 0
        else:
            raise e
    return file_size

def get_current_storage_usage():
    """ determine the available size of the device running the server. """
    # Get the total disk space
    total_space = os.statvfs("/").f_blocks * os.statvfs("/").f_frsize
    # Get the free disk space
    free_space = os.statvfs("/").f_bavail * os.statvfs("/").f_frsize
    # Calculate the used disk space
    used_space = total_space - free_space
    return used_space

def get_all_files():
    """ This loads all files in the data folder, returning the file path. """
    all_files = []
    for root, directories, files in os.walk(DATA_BASE):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isdir(file_path) is False:
                all_files.append(file_path)      
    return all_files

def garbage_collect(max_storage_mb):
    """ Delete files from the data folder when memory is exceeded. """
    max_storage_usage = max_storage_mb * 1024 * 1024  # Convert MB to bytes
    current_storage_usage = get_current_storage_usage()
    if current_storage_usage > max_storage_usage:
        files = get_all_files()
        files = sorted(files, key=lambda f: os.path.getmtime(f), reverse=True)
        while current_storage_usage > max_storage_usage and len(files) > 0:
            file_to_delete = files.pop()
            file_size = os.path.getsize(file_to_delete)
            try:
                os.remove(file_to_delete)
            except OSError as e:
                print(f"Failed to delete file: {file_to_delete}")
            current_storage_usage -= file_size