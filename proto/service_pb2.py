# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: proto/service.proto
# Protobuf Python Version: 5.29.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    2,
    '',
    'proto/service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13proto/service.proto\"$\n\x0eReceiptRequest\x12\x12\n\nimage_data\x18\x01 \x01(\x0c\"(\n\x0f\x43lassifyRequest\x12\x15\n\rproducts_json\x18\x01 \x01(\t\"#\n\x0bTop5Request\x12\x14\n\x0cproduct_json\x18\x01 \x01(\t\"@\n\x10ProcessingResult\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\x12\r\n\x05\x65rror\x18\x03 \x01(\t2\xab\x01\n\tPipelines\x12\x34\n\x0eProcessReceipt\x12\x0f.ReceiptRequest\x1a\x11.ProcessingResult\x12\x37\n\x10\x43lassifyProducts\x12\x10.ClassifyRequest\x1a\x11.ProcessingResult\x12/\n\x0cTop5Products\x12\x0c.Top5Request\x1a\x11.ProcessingResultb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RECEIPTREQUEST']._serialized_start=23
  _globals['_RECEIPTREQUEST']._serialized_end=59
  _globals['_CLASSIFYREQUEST']._serialized_start=61
  _globals['_CLASSIFYREQUEST']._serialized_end=101
  _globals['_TOP5REQUEST']._serialized_start=103
  _globals['_TOP5REQUEST']._serialized_end=138
  _globals['_PROCESSINGRESULT']._serialized_start=140
  _globals['_PROCESSINGRESULT']._serialized_end=204
  _globals['_PIPELINES']._serialized_start=207
  _globals['_PIPELINES']._serialized_end=378
# @@protoc_insertion_point(module_scope)
