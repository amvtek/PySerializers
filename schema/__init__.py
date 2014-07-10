#  -*- coding: utf-8 -*-

__all__ = ['get_protostuff', 'get_thriftstuff']

class StuffToTestSchema(object):
    "index protobuf/thrift generated message classes"

    FRAMEWORK = frozenset(['protobuf','thrift'])
    
    def __init__(self, modul, framework, comp_version):

        # import compiled message classes
        for name in ['NumStuff', 'StringStuff', 'ComboStuff', 'ComboBunch']:
            
            msgClass = getattr(modul, name)
            setattr(self, name, msgClass)

        # validate framework
        if framework not in self.FRAMEWORK:
            raise ValueError("Invalid framework!")
        self.framework = framework

        # validate compiler version
        self.version = comp_version

    def __hash__(self):

        return hash((self.framework, self.version))

# index protobuf version of StuffToTest schema
def get_protostuff():
    "return protoc compiled message classes for StuffToTest schema"

    import proto_2_5_0.StuffToTest_pb2 as m1
    return StuffToTestSchema(m1,'protobuf',(2,5,0))

# index thrift version of StuffToTest schema
def get_thriftstuff():
    "return thrift compiled message classes for StuffToTest schema"

    import thrift_0_9_0.StuffToTest.constants as m2
    return StuffToTestSchema(m2,'thrift',(0,9,0))
