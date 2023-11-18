import concurrent.futures
import HitchhikerSource_pb2
import HitchhikerSource_pb2_grpc
import grpc
import time

from helper import extract_file_content, file_is_delivered, remove_sourse_file, garbage_collect, get_downloads

server_source = "pilot04"

class HitchhikerSourceServicer(HitchhikerSource_pb2_grpc.HitchhikerSourceServicer):

    def GetSourceId(self, request, context):
        source_id = server_source
        response = HitchhikerSource_pb2.SourceIdResponse(source_id=source_id)
        return response

    def GetDownloads(self, request, context):
        client_id = request.client_id
        destination_id = request.destination_id
        available_files = get_downloads(client_id, destination_id)
        response = HitchhikerSource_pb2.DownloadListResponse(
            file_list=available_files)
        return response

    def DownloadFile(self, request, context):
        client_id = request.client_id
        file_ids = request.file_list
        downloaded_files = []
        for file_id in file_ids:
            file = extract_file_content(file_id, client_id)
            downloaded_files.append(file)
        response = HitchhikerSource_pb2.DownloadFileResponse(
            file=downloaded_files)
        return response

    def MarkDelivered(self, request, context):
        client_id = request.client_id
        destination_id = request.destination_id
        file_ids = request.file_list
        for file_id in file_ids:
            if file_is_delivered(file_id, destination_id):
                remove_sourse_file(file_id, client_id)
        delivery_status = "Files delivered successfully"
        response = HitchhikerSource_pb2.DeliveryStatusResponse(
            status=delivery_status)
        return response

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    hitchhiker_source_servicer = HitchhikerSourceServicer()
    HitchhikerSource_pb2_grpc.add_HitchhikerSourceServicer_to_server(
        hitchhiker_source_servicer, server)
    server.add_insecure_port('[::]:50051')
    server.start()

    garbage_collection_interval = 60 * 60  # Run garbage collection every hour
    while True:
        time.sleep(garbage_collection_interval)
        garbage_collect(100)

if __name__ == '__main__':
    serve()
