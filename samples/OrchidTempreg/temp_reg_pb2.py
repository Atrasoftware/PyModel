# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temp_reg.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='temp_reg.proto',
  package='temp_reg',
  syntax='proto3',
  serialized_pb=_b('\n\x0etemp_reg.proto\x12\x08temp_reg\"\x11\n\x03TId\x12\n\n\x02id\x18\x01 \x01(\x05\"^\n\x08TConfigs\x12\n\n\x02id\x18\x01 \x01(\x05\x12\n\n\x02sp\x18\x02 \x01(\x02\x12\t\n\x01p\x18\x03 \x01(\x02\x12\t\n\x01i\x18\x04 \x01(\x02\x12\t\n\x01\x64\x18\x05 \x01(\x02\x12\x0c\n\x04name\x18\x06 \x01(\t\x12\x0b\n\x03run\x18\x07 \x01(\x08\">\n\x0cTemperatures\x12\n\n\x02t0\x18\x01 \x01(\x02\x12\n\n\x02t1\x18\x02 \x01(\x02\x12\n\n\x02t2\x18\x03 \x01(\x02\x12\n\n\x02t3\x18\x04 \x01(\x02\"\x07\n\x05\x45mpty2\x90\x02\n\x04TReg\x12\x31\n\nSetConfigs\x12\x12.temp_reg.TConfigs\x1a\x0f.temp_reg.Empty\x12?\n\x12StreamTemperatures\x12\x0f.temp_reg.Empty\x1a\x16.temp_reg.Temperatures0\x01\x12\x31\n\x0fStartRegulators\x12\r.temp_reg.TId\x1a\x0f.temp_reg.Empty\x12\x30\n\x0eStopRegulators\x12\r.temp_reg.TId\x1a\x0f.temp_reg.Empty\x12/\n\nGetConfigs\x12\r.temp_reg.TId\x1a\x12.temp_reg.TConfigsb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_TID = _descriptor.Descriptor(
  name='TId',
  full_name='temp_reg.TId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='temp_reg.TId.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=28,
  serialized_end=45,
)


_TCONFIGS = _descriptor.Descriptor(
  name='TConfigs',
  full_name='temp_reg.TConfigs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='temp_reg.TConfigs.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sp', full_name='temp_reg.TConfigs.sp', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='p', full_name='temp_reg.TConfigs.p', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='i', full_name='temp_reg.TConfigs.i', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='d', full_name='temp_reg.TConfigs.d', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='temp_reg.TConfigs.name', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='run', full_name='temp_reg.TConfigs.run', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=47,
  serialized_end=141,
)


_TEMPERATURES = _descriptor.Descriptor(
  name='Temperatures',
  full_name='temp_reg.Temperatures',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='t0', full_name='temp_reg.Temperatures.t0', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='t1', full_name='temp_reg.Temperatures.t1', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='t2', full_name='temp_reg.Temperatures.t2', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='t3', full_name='temp_reg.Temperatures.t3', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=205,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='temp_reg.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=207,
  serialized_end=214,
)

DESCRIPTOR.message_types_by_name['TId'] = _TID
DESCRIPTOR.message_types_by_name['TConfigs'] = _TCONFIGS
DESCRIPTOR.message_types_by_name['Temperatures'] = _TEMPERATURES
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY

TId = _reflection.GeneratedProtocolMessageType('TId', (_message.Message,), dict(
  DESCRIPTOR = _TID,
  __module__ = 'temp_reg_pb2'
  # @@protoc_insertion_point(class_scope:temp_reg.TId)
  ))
_sym_db.RegisterMessage(TId)

TConfigs = _reflection.GeneratedProtocolMessageType('TConfigs', (_message.Message,), dict(
  DESCRIPTOR = _TCONFIGS,
  __module__ = 'temp_reg_pb2'
  # @@protoc_insertion_point(class_scope:temp_reg.TConfigs)
  ))
_sym_db.RegisterMessage(TConfigs)

Temperatures = _reflection.GeneratedProtocolMessageType('Temperatures', (_message.Message,), dict(
  DESCRIPTOR = _TEMPERATURES,
  __module__ = 'temp_reg_pb2'
  # @@protoc_insertion_point(class_scope:temp_reg.Temperatures)
  ))
_sym_db.RegisterMessage(Temperatures)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'temp_reg_pb2'
  # @@protoc_insertion_point(class_scope:temp_reg.Empty)
  ))
_sym_db.RegisterMessage(Empty)


import grpc
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities


class TRegStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SetConfigs = channel.unary_unary(
        '/temp_reg.TReg/SetConfigs',
        request_serializer=TConfigs.SerializeToString,
        response_deserializer=Empty.FromString,
        )
    self.StreamTemperatures = channel.unary_stream(
        '/temp_reg.TReg/StreamTemperatures',
        request_serializer=Empty.SerializeToString,
        response_deserializer=Temperatures.FromString,
        )
    self.StartRegulators = channel.unary_unary(
        '/temp_reg.TReg/StartRegulators',
        request_serializer=TId.SerializeToString,
        response_deserializer=Empty.FromString,
        )
    self.StopRegulators = channel.unary_unary(
        '/temp_reg.TReg/StopRegulators',
        request_serializer=TId.SerializeToString,
        response_deserializer=Empty.FromString,
        )
    self.GetConfigs = channel.unary_unary(
        '/temp_reg.TReg/GetConfigs',
        request_serializer=TId.SerializeToString,
        response_deserializer=TConfigs.FromString,
        )


class TRegServicer(object):

  def SetConfigs(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StreamTemperatures(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StartRegulators(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def StopRegulators(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetConfigs(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TRegServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SetConfigs': grpc.unary_unary_rpc_method_handler(
          servicer.SetConfigs,
          request_deserializer=TConfigs.FromString,
          response_serializer=Empty.SerializeToString,
      ),
      'StreamTemperatures': grpc.unary_stream_rpc_method_handler(
          servicer.StreamTemperatures,
          request_deserializer=Empty.FromString,
          response_serializer=Temperatures.SerializeToString,
      ),
      'StartRegulators': grpc.unary_unary_rpc_method_handler(
          servicer.StartRegulators,
          request_deserializer=TId.FromString,
          response_serializer=Empty.SerializeToString,
      ),
      'StopRegulators': grpc.unary_unary_rpc_method_handler(
          servicer.StopRegulators,
          request_deserializer=TId.FromString,
          response_serializer=Empty.SerializeToString,
      ),
      'GetConfigs': grpc.unary_unary_rpc_method_handler(
          servicer.GetConfigs,
          request_deserializer=TId.FromString,
          response_serializer=TConfigs.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'temp_reg.TReg', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BetaTRegServicer(object):
  """The Beta API is deprecated for 0.15.0 and later.

  It is recommended to use the GA API (classes and functions in this
  file not marked beta) for all further purposes. This class was generated
  only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
  def SetConfigs(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def StreamTemperatures(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def StartRegulators(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def StopRegulators(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def GetConfigs(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


class BetaTRegStub(object):
  """The Beta API is deprecated for 0.15.0 and later.

  It is recommended to use the GA API (classes and functions in this
  file not marked beta) for all further purposes. This class was generated
  only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
  def SetConfigs(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  SetConfigs.future = None
  def StreamTemperatures(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  def StartRegulators(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  StartRegulators.future = None
  def StopRegulators(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  StopRegulators.future = None
  def GetConfigs(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
    raise NotImplementedError()
  GetConfigs.future = None


def beta_create_TReg_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  """The Beta API is deprecated for 0.15.0 and later.

  It is recommended to use the GA API (classes and functions in this
  file not marked beta) for all further purposes. This function was
  generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
  request_deserializers = {
    ('temp_reg.TReg', 'GetConfigs'): TId.FromString,
    ('temp_reg.TReg', 'SetConfigs'): TConfigs.FromString,
    ('temp_reg.TReg', 'StartRegulators'): TId.FromString,
    ('temp_reg.TReg', 'StopRegulators'): TId.FromString,
    ('temp_reg.TReg', 'StreamTemperatures'): Empty.FromString,
  }
  response_serializers = {
    ('temp_reg.TReg', 'GetConfigs'): TConfigs.SerializeToString,
    ('temp_reg.TReg', 'SetConfigs'): Empty.SerializeToString,
    ('temp_reg.TReg', 'StartRegulators'): Empty.SerializeToString,
    ('temp_reg.TReg', 'StopRegulators'): Empty.SerializeToString,
    ('temp_reg.TReg', 'StreamTemperatures'): Temperatures.SerializeToString,
  }
  method_implementations = {
    ('temp_reg.TReg', 'GetConfigs'): face_utilities.unary_unary_inline(servicer.GetConfigs),
    ('temp_reg.TReg', 'SetConfigs'): face_utilities.unary_unary_inline(servicer.SetConfigs),
    ('temp_reg.TReg', 'StartRegulators'): face_utilities.unary_unary_inline(servicer.StartRegulators),
    ('temp_reg.TReg', 'StopRegulators'): face_utilities.unary_unary_inline(servicer.StopRegulators),
    ('temp_reg.TReg', 'StreamTemperatures'): face_utilities.unary_stream_inline(servicer.StreamTemperatures),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)


def beta_create_TReg_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  """The Beta API is deprecated for 0.15.0 and later.

  It is recommended to use the GA API (classes and functions in this
  file not marked beta) for all further purposes. This function was
  generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
  request_serializers = {
    ('temp_reg.TReg', 'GetConfigs'): TId.SerializeToString,
    ('temp_reg.TReg', 'SetConfigs'): TConfigs.SerializeToString,
    ('temp_reg.TReg', 'StartRegulators'): TId.SerializeToString,
    ('temp_reg.TReg', 'StopRegulators'): TId.SerializeToString,
    ('temp_reg.TReg', 'StreamTemperatures'): Empty.SerializeToString,
  }
  response_deserializers = {
    ('temp_reg.TReg', 'GetConfigs'): TConfigs.FromString,
    ('temp_reg.TReg', 'SetConfigs'): Empty.FromString,
    ('temp_reg.TReg', 'StartRegulators'): Empty.FromString,
    ('temp_reg.TReg', 'StopRegulators'): Empty.FromString,
    ('temp_reg.TReg', 'StreamTemperatures'): Temperatures.FromString,
  }
  cardinalities = {
    'GetConfigs': cardinality.Cardinality.UNARY_UNARY,
    'SetConfigs': cardinality.Cardinality.UNARY_UNARY,
    'StartRegulators': cardinality.Cardinality.UNARY_UNARY,
    'StopRegulators': cardinality.Cardinality.UNARY_UNARY,
    'StreamTemperatures': cardinality.Cardinality.UNARY_STREAM,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'temp_reg.TReg', cardinalities, options=stub_options)
# @@protoc_insertion_point(module_scope)
