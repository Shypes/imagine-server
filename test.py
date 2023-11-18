import unittest
import grpc
import HitchhikerSource_pb2
import HitchhikerSource_pb2_grpc

class HitchhikerSourceServicerTest(unittest.TestCase):

    def setUp(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = HitchhikerSource_pb2_grpc.HitchhikerSourceStub(self.channel)

    def tearDown(self):
        self.channel.close()

    def test_get_source_id(self):
        request = HitchhikerSource_pb2.SourceIdResponse()
        response = self.stub.GetSourceId(request)
        self.assertEqual(response.source_id, "pilot04")

    def test_get_downloads(self):
        request = HitchhikerSource_pb2.ClientDownloadRequest(client_id="client01", destination_id="befit_1")
        response = self.stub.GetDownloads(request, timeout=None)
        available_files = response.file_list
        self.assertEqual(len(available_files), 2)

    def test_download_file(self):
        request = HitchhikerSource_pb2.DownloadFileRequest(client_id="client01", file_list=["2.txt"])
        response = self.stub.DownloadFile(request, timeout=None)
        downloaded_files = response.file       
        self.assertEqual(len(list(downloaded_files)), 1)
        self.assertEqual(downloaded_files[0].file_id, "2.txt")
        self.assertEqual(downloaded_files[0].file_name, "2.txt")
        self.assertEqual(downloaded_files[0].file_type, ".txt")

    def test_mark_delivered(self):
        request = HitchhikerSource_pb2.ClientDeliveryRequest(client_id="client01", destination_id="befit_1", file_list=["3.txt"])
        response = self.stub.MarkDelivered(request, timeout=None)
        self.assertEqual(response.status, "Files delivered successfully")

if __name__ == "__main__":
    unittest.main()