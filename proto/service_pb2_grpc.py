# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from proto import service_pb2 as proto_dot_service__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in proto/service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class PipelinesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessReceipt = channel.unary_unary(
                '/Pipelines/ProcessReceipt',
                request_serializer=proto_dot_service__pb2.ReceiptRequest.SerializeToString,
                response_deserializer=proto_dot_service__pb2.ProcessingResult.FromString,
                _registered_method=True)
        self.ClassifyProducts = channel.unary_unary(
                '/Pipelines/ClassifyProducts',
                request_serializer=proto_dot_service__pb2.ClassifyRequest.SerializeToString,
                response_deserializer=proto_dot_service__pb2.ProcessingResult.FromString,
                _registered_method=True)
        self.Top5Products = channel.unary_unary(
                '/Pipelines/Top5Products',
                request_serializer=proto_dot_service__pb2.Top5Request.SerializeToString,
                response_deserializer=proto_dot_service__pb2.ProcessingResult.FromString,
                _registered_method=True)


class PipelinesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ProcessReceipt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClassifyProducts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Top5Products(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PipelinesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProcessReceipt': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessReceipt,
                    request_deserializer=proto_dot_service__pb2.ReceiptRequest.FromString,
                    response_serializer=proto_dot_service__pb2.ProcessingResult.SerializeToString,
            ),
            'ClassifyProducts': grpc.unary_unary_rpc_method_handler(
                    servicer.ClassifyProducts,
                    request_deserializer=proto_dot_service__pb2.ClassifyRequest.FromString,
                    response_serializer=proto_dot_service__pb2.ProcessingResult.SerializeToString,
            ),
            'Top5Products': grpc.unary_unary_rpc_method_handler(
                    servicer.Top5Products,
                    request_deserializer=proto_dot_service__pb2.Top5Request.FromString,
                    response_serializer=proto_dot_service__pb2.ProcessingResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Pipelines', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('Pipelines', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Pipelines(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ProcessReceipt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Pipelines/ProcessReceipt',
            proto_dot_service__pb2.ReceiptRequest.SerializeToString,
            proto_dot_service__pb2.ProcessingResult.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ClassifyProducts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Pipelines/ClassifyProducts',
            proto_dot_service__pb2.ClassifyRequest.SerializeToString,
            proto_dot_service__pb2.ProcessingResult.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Top5Products(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/Pipelines/Top5Products',
            proto_dot_service__pb2.Top5Request.SerializeToString,
            proto_dot_service__pb2.ProcessingResult.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
