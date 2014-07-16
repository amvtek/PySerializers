#  -*- coding: utf-8 -*-

from os.path import abspath, dirname, join

__all__ = ['get_protostuff', 'get_thriftstuff', 'get_capnpstuff']

PROJECT_ROOT = dirname(dirname(abspath(__file__)))

FNIDX = [
        ('NumStuff',
            ('i01','i02','d03','l1_i05','l1_d06','l1_e07')),
        ('StringStuff',
            ('s01','b02','l1_s03','l1_b04')),
        ('ComboStuff',
            ('i01','i02','d03','l1_i05','l1_d06','l1_e07','s08','b09','l1_s10','l1_b11')),
        ('ComboBunch',
            ('e_01','ns02','ss03','cs04','l2_ns05','l2_ss06','l2_cs07'))
        ]

class SchemaContainer(object):
    "holds references to StuffToTest messages..."

    def __init__(self, framework, version):
        
        self.framework = framework

        self.version = version

    def __hash__(self):

        return hash((self.framework, self.version))

class StuffToTestPTSchema(object):
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

class CapNpStructProxy(object):
    "provide factory delivering initialized instances of CapNp struct"

    def __init__(self, structClass, *benchargs):

        # set proxied struct 
        self.struct = structClass

        # renameIdx maps name normally used for message fields in benchmark
        # to name compatible with capnp naming conventions
        # the hurdle is that capnp only supports CamelCase...
        self._renameIdx = {a:a.lower().replace('_','') for a in benchargs}

    def rename_keys(self, dico):
        "return dict with key names adapted to proxied capnp struct"

        rn = self._renameIdx.get # local alias
        return {rn(k,k):v for k,v in dico.items()}

    def __call__(self, **kwargs):
        "return proxied capnp struct instance"

        capArgs = self.rename_keys(kwargs)
        return self.struct.new_message(**capArgs)


# index protobuf version of StuffToTest schema
def get_protostuff():
    "return protoc compiled message classes for StuffToTest schema"

    import proto_2_5_0.StuffToTest_pb2 as m1
    return StuffToTestPTSchema(m1,'protobuf',(2,5,0))

# index thrift version of StuffToTest schema
def get_thriftstuff():
    "return thrift compiled message classes for StuffToTest schema"

    import thrift_0_9_0.StuffToTest.constants as m2
    return StuffToTestPTSchema(m2,'thrift',(0,9,0))

# index capnp version of StuffToTest schema
def get_pycapnpstuff():
    "return capnp adapted message factories for StuffToTest schema"

    # loads the StuffToTest schema
    import capnp
    capnp.remove_import_hook()
    schmod = capnp.load(join(PROJECT_ROOT,'idl/StuffToTest.capnp'))

    # contruct schema
    schema = SchemaContainer('pycapnp', capnp.__version__)

    for message, fieldnames in FNIDX:

        # load capnp Struct class
        structClass = getattr(schmod,message)

        # contruct Struct proxy object
        structProxy = CapNpStructProxy(structClass,*fieldnames)

        # add proxy to schema
        setattr(schema, message, structProxy)

    return schema
