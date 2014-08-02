#  -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    utilities to support comparing python implementation 
    of serialization frameworks

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

def is_protobuf_available(with_extension=False):
    "return True if selected protobuf framework is reachable"

    try:

        if with_extension:
            
            #TODO : OK for protobuf 2.5.0
            #TODO : not clean as private modules are not public API...
            import google.protobuf.internal._net_proto2___python

        else:

            import google.protobuf

        return True

    except ImportError:

        return False

def build_protobuf_serializer():
    "return callable serializing protobuf message object"

    def serialize(protoobj):

        return protoobj.SerializeToString()

    return serialize


def build_protobuf_deserializer(Msg, with_extension=False):
    "return callable deserializing message encoding MsgClass"

    MsgClass = Msg.struct

    def deserialize(data):

        rv = MsgClass()
        rv.ParseFromString(data)
        return rv
    
    return deserialize

def is_thrift_available(with_extension=False):
    "return True if selected thrift framework is reachable"

    try:

        if with_extension:

            from thrift.protocol import fastbinary
            if not fastbinary:
                raise ImportError("fastbinary not available")

        else:

            import thrift.protocol

        return True

    except:

        return False

def build_thrift_serializer(with_extension=False):
    "return callable serializing thrift struct object"

    from thrift.protocol import TBinaryProtocol
    from thrift.transport import TTransport

    # set Transport
    Transport = TTransport.TMemoryBuffer

    # select Protocol
    if with_extension:
        Protocol = TBinaryProtocol.TBinaryProtocolAccelerated
    else:
        Protocol = TBinaryProtocol.TBinaryProtocol

    def serialize(thriftobj):

        tout = Transport()
        thriftobj.write(Protocol(tout))
        return tout.getvalue()

    return serialize

def build_thrift_deserializer(Msg, with_extension=False):
    "return callable deserializing message encoding StructClass"
    
    from thrift.protocol import TBinaryProtocol
    from thrift.transport import TTransport

    # set Transport
    Transport = TTransport.TMemoryBuffer

    # select Protocol
    if with_extension:
        Protocol = TBinaryProtocol.TBinaryProtocolAccelerated
    else:
        Protocol = TBinaryProtocol.TBinaryProtocol

    StructClass = Msg.struct

    def deserialize(data):
        
        msg = StructClass()
        msg.read(Protocol(Transport(data)))
        msg.validate()
        return msg

    return deserialize

def is_pycapnp_available(ignored=False):
    "return True if pycapnp can be imported"

    try:
        import capnp
        return True

    except:

        return False

def build_pycapnp_serializer():
    "return callable serializing pycapnp message object"

    def serialize(capnpobj):

        return capnpobj.to_bytes()

    return serialize


def build_pycapnp_deserializer(Msg, ignored=False):
    "return callable deserializing message encoding Msg.struct"

    MsgClass = Msg.struct

    def deserialize(data):

        return MsgClass.from_bytes(data)
    
    return deserialize

def is_json_available(ignored=False):
    "return True if json can be imported"

    try:
        import json
        return True
    except:
        return False

def is_sjson_available(ignored=False):
    "return True if simplejson can be imported"

    try:
        import simplejson
        return True
    except:
        return False

def is_ujson_available(ignored=False):
    "return True if ujson can be imported"

    try:
        import ujson
        return True
    except:
        return False

def build_json_serializer():
    "return json.dumps callable"

    from json import dumps

    return dumps

def build_sjson_serializer():
    "return simplejson.dumps callable"

    from simplejson import dumps

    return dumps

def build_ujson_serializer():
    "return ujson.dumps callable"

    from ujson import dumps

    return dumps

def build_json_deserializer(Msg, ignored=False):
    "return json.loads callable"

    from json import loads

    return loads

def build_sjson_deserializer(Msg, ignored=False):
    "return json.loads callable"

    from simplejson import loads

    return loads

def build_ujson_deserializer(Msg, ignored=False):
    "return json.loads callable"

    from ujson import loads

    return loads

def is_msgpack_available(ignored=False):
    "return True if msgpack can be imported"

    try:
        import msgpack
        return True
    except:
        return False

def build_msgpack_serializer():
    "return msgpack.dumps callable"

    from msgpack import dumps

    return dumps

def build_msgpack_deserializer(Msg, ignored=False):
    "return msgpack.loads callable"

    from msgpack import loads
    from functools import partial

    return partial(loads,use_list=0)
