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


def build_protobuf_deserializer(MsgClass, with_extension=False):
    "return callable deserializing message encoding MsgClass"

    def deserialize(data):

        return MsgClass().ParseFromString(data)
    
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

def build_thrift_deserializer(StructClass, with_extension=False):
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
