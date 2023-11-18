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