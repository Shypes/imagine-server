# Router communication server

This is a sample communication server built using gRPC using a proto file.

## Assumptions Made
- Files are stored in a designated folder called data.

- The server source is in a static folder in the data folder.

- A client will have a unique folder within the dedicated folder.

- The client folder will have two major folders: source and destination. Data is moved from the source folder to the destination folder with the client folder.


#### Our goal is to implement the gRPC server, which allows the client to operate on the server using the predefined structure of the proto file.


### How to run the code

The code is written in Python 3.

The required Python libraries can be found in the requirements.txt file.

Can be installed using this command.

``` 
pip install -R requirements.txt
```

Once libary is installed, you can generate the gRPC file using this command.

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. HitchhikerSource.proto
```

Note that this has already been generated for this project.


#### Start the gRPC server using the Python code below.

```
python MetricsLocal.py
```

This will start the server on port `50051`. Ensure that this port is available.

### Run the unit test to test the server.

```
python test.py
```

Note that if the server keeps running for over an hour based on the current code settings, files in the data folder might be deleted as the garbage collector checks for the file space of 100 MB.


This will cause the unit test to fail.

To get the deleted files back, navigate to the client source folder.


```
cd data/pilot04/source/client01
```


Then run the command below.


```
touch 1.txt
touch 2.txt
touch 3.txt
```


If the files are deleted and the above steps are carried out to create the file, the unit test will fail on the first run and pass on the second.

`I was able to successfully run the code on my Mac Laptop with out needing OpenWRT Virtual machine`