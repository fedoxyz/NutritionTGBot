import grpc.aio
from proto.service_pb2 import ReceiptRequest, ClassifyRequest, ProcessingResult, Top5Request
from proto.service_pb2_grpc import PipelinesStub
from config import GRPC_SERVER
from logger import logger

class GRPCClient:
    _instance = None
    _lock = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            while cls._lock:
                pass
            cls._lock = True
            try:
                if cls._instance is None:
                    cls._instance = super(GRPCClient, cls).__new__(cls, *args, **kwargs)
                    cls._instance._initialize_channel_and_stub()
            finally:
                cls._lock = False
        return cls._instance

    def _initialize_channel_and_stub(self):
        self.channel = grpc.aio.insecure_channel(GRPC_SERVER)
        self.stub = PipelinesStub(self.channel)

    async def process_receipt(self, image_data):
        request = ReceiptRequest(image_data=image_data)
        response = await self.stub.ProcessReceipt(request)
        return response

    async def classify_products(self, products_json):
        request = ClassifyRequest(products_json=products_json)
        response = await self.stub.ClassifyProducts(request)
        return response

    async def top_5_products(self, product_json):
        request = Top5Request(product_json=product_json)
        response = await self.stub.Top5Products(request)
        return response
