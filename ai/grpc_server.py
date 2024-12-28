import grpc
from concurrent import futures
import json
from typing import Callable

from proto.service_pb2 import ReceiptRequest, ClassifyRequest, ProcessingResult
from proto.service_pb2_grpc import PipelinesServicer, add_PipelinesServicer_to_server
from pipelines import process_receipt, classify_ollama_receipt_products, classify_receipt_keras, classify_receipt_bert
from logger import logger
from utils import postprocess_keras_preds, postprocess_bert_preds

def convert_result(result) -> ProcessingResult:
    """Convert internal result to ProcessingResult proto message."""
    try:
        # Convert data to string if it's not already
        data_str = (
            json.dumps(result.data, ensure_ascii=False) 
            if not isinstance(result.data, str) 
            else result.data
        )
        
        return ProcessingResult(
            success=result.success,
            data=data_str,
            error=result.error
        )
    except Exception as e:
        logger.error(f"Error converting result: {str(e)}")
        return ProcessingResult(
            success=False,
            data="",
            error=f"Error converting result: {str(e)}"
        )

def process_receipt_handler(request: ReceiptRequest, context) -> ProcessingResult:
    """Handle receipt processing requests."""
    try:
        result = process_receipt(request.image_data)
        return convert_result(result)
    except Exception as e:
        logger.error(f"Error processing receipt: {str(e)}")
        return ProcessingResult(
            success=False,
            data="",
            error=f"Error processing receipt: {str(e)}"
        )

def classify_products_handler(request: ClassifyRequest, context) -> ProcessingResult:
    """Handle product classification requests."""
    try:
        logger.debug("Starting products classification")
        logger.debug(f"request - {request}")
        products = json.loads(request.products_json)
        result = classify_receipt_bert(products)
        logger.debug(result)
        result.data = postprocess_bert_preds(result.data)
        logger.debug(result.data)
        return convert_result(result)
    except Exception as e:
        logger.error(f"Error classifying products: {str(e)}")
        return ProcessingResult(
            success=False,
            data="",
            error=f"Error classifying products: {str(e)}"
        )

def create_servicer(
    process_receipt_fn: Callable = process_receipt_handler,
    classify_products_fn: Callable = classify_products_handler
) -> PipelinesServicer:
    """Create a PipelinesServicer with the specified handler functions."""
    
    class FunctionalPipelinesServicer(PipelinesServicer):
        def ProcessReceipt(self, request, context):
            return process_receipt_fn(request, context)
            
        def ClassifyProducts(self, request, context):
            return classify_products_fn(request, context)
    
    return FunctionalPipelinesServicer()

def serve():
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Create and add the servicer to the server
    servicer = create_servicer()
    add_PipelinesServicer_to_server(servicer, server)
    
    # Listen on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    
    logger.info("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
