# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mservice.proto

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
  name='mservice.proto',
  package='mservice',
  syntax='proto3',
  serialized_pb=_b('\n\x0emservice.proto\x12\x08mservice\"\'\n\tCommunity\x12\x0b\n\x03\x61sn\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x05\"\x8d\x01\n\x0eMformatMessage\x12\x0f\n\x07service\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0e\n\x06prefix\x18\x03 \x01(\t\x12\x0f\n\x07\x61s_path\x18\x04 \x03(\x05\x12(\n\x0b\x63ommunities\x18\x05 \x03(\x0b\x32\x13.mservice.Community\x12\x11\n\ttimestamp\x18\x06 \x01(\x01\"\x07\n\x05\x45mpty2N\n\x0fMessageListener\x12;\n\x0cqueryMformat\x12\x18.mservice.MformatMessage\x1a\x0f.mservice.Empty\"\x00\x42\x32\n\x16\x61rtemis.io.grpc.protosB\rMServiceProtoP\x01\xa2\x02\x06MSRVCPb\x06proto3')
)




_COMMUNITY = _descriptor.Descriptor(
  name='Community',
  full_name='mservice.Community',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='asn', full_name='mservice.Community.asn', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='mservice.Community.value', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_end=67,
)


_MFORMATMESSAGE = _descriptor.Descriptor(
  name='MformatMessage',
  full_name='mservice.MformatMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='service', full_name='mservice.MformatMessage.service', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='mservice.MformatMessage.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='prefix', full_name='mservice.MformatMessage.prefix', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='as_path', full_name='mservice.MformatMessage.as_path', index=3,
      number=4, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='communities', full_name='mservice.MformatMessage.communities', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='mservice.MformatMessage.timestamp', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
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
  serialized_start=70,
  serialized_end=211,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='mservice.Empty',
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
  serialized_start=213,
  serialized_end=220,
)

_MFORMATMESSAGE.fields_by_name['communities'].message_type = _COMMUNITY
DESCRIPTOR.message_types_by_name['Community'] = _COMMUNITY
DESCRIPTOR.message_types_by_name['MformatMessage'] = _MFORMATMESSAGE
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Community = _reflection.GeneratedProtocolMessageType('Community', (_message.Message,), dict(
  DESCRIPTOR = _COMMUNITY,
  __module__ = 'mservice_pb2'
  # @@protoc_insertion_point(class_scope:mservice.Community)
  ))
_sym_db.RegisterMessage(Community)

MformatMessage = _reflection.GeneratedProtocolMessageType('MformatMessage', (_message.Message,), dict(
  DESCRIPTOR = _MFORMATMESSAGE,
  __module__ = 'mservice_pb2'
  # @@protoc_insertion_point(class_scope:mservice.MformatMessage)
  ))
_sym_db.RegisterMessage(MformatMessage)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'mservice_pb2'
  # @@protoc_insertion_point(class_scope:mservice.Empty)
  ))
_sym_db.RegisterMessage(Empty)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\026artemis.io.grpc.protosB\rMServiceProtoP\001\242\002\006MSRVCP'))

_MESSAGELISTENER = _descriptor.ServiceDescriptor(
  name='MessageListener',
  full_name='mservice.MessageListener',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=222,
  serialized_end=300,
  methods=[
  _descriptor.MethodDescriptor(
    name='queryMformat',
    full_name='mservice.MessageListener.queryMformat',
    index=0,
    containing_service=None,
    input_type=_MFORMATMESSAGE,
    output_type=_EMPTY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MESSAGELISTENER)

DESCRIPTOR.services_by_name['MessageListener'] = _MESSAGELISTENER

# @@protoc_insertion_point(module_scope)
