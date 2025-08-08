from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SNMPRequest(_message.Message):
    __slots__ = ("ip", "oid", "community", "version")
    IP_FIELD_NUMBER: _ClassVar[int]
    OID_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ip: str
    oid: str
    community: str
    version: int
    def __init__(self, ip: _Optional[str] = ..., oid: _Optional[str] = ..., community: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class SNMPResponse(_message.Message):
    __slots__ = ("value", "status")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    value: str
    status: str
    def __init__(self, value: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
