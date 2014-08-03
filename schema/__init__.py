#  -*- coding: utf-8 -*-

import importlib
from functools import partial
from os.path import abspath, dirname, join

__all__ = [
        'get_jsonstuff',
        'get_msgpackstuff',
        'get_protostuff',
        'get_thriftstuff',
        'get_capnpstuff'
        ]

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

version_string = lambda vtuple:"%s.%s.%s"%vtuple

class SchemaContainer(object):
    "holds references to StuffToTest messages..."

    def __init__(self, framework, version):
        
        self.framework = framework

        self.version = version

    def __hash__(self):

        return hash((self.framework, self.version))

class StructProxy(object):
    "provide factory delivering initialized instances of struct"

    _factoryIdx = {
            'ns':lambda ctx:ctx['NumStuff'],
            'ss':lambda ctx:ctx['StringStuff'],
            'cs':lambda ctx:ctx['ComboStuff'],
            }

    def _map_factory(self,func):
        "return callable that map func to sequence argument"

        return lambda seq:map(func,seq)

    def __init__(self, structClass, fieldnames, context=None):

        maf = self._map_factory # local alias
        noop = lambda v:v
        
        # set proxied struct 
        self.struct = structClass
        self.make_struct = structClass

        # fill contruct & read indexes
        factoryIdx = self._factoryIdx

        constructIdx = {}
        prepareIdx = {}
        readIdx = {}
        
        for fld in fieldnames:
            
            # read field prefix selector
            fps = fld[:2]

            if fps in factoryIdx :
                
                # field is a struct
                
                factory = factoryIdx[fps](context)

                constructIdx[fld] = factory.newobj
                prepareIdx[fld] = factory.prepare
                readIdx[fld] = factory.todict

            elif fps == 'l1':

                # field is a list of values
                
                readIdx[fld] = list

            elif fps == 'l2':

                # field is a list of struct

                # read field inner selector
                fis = fld.replace('_','')[2:4]

                factory = factoryIdx[fis](context)

                constructIdx[fld] = maf(factory.newobj)
                prepareIdx[fld] = maf(factory.prepare)
                readIdx[fld] = maf(factory.todict)

            else:
                
                # field is a value

                readIdx[fld] = lambda msgfld:msgfld

        # set newobj
        if constructIdx:
            self.newobj = self.construct_processing_inner_fields
        else:
            self.newobj = self.construct

        self.constructIdx = constructIdx.items()
        self.prepareIdx = prepareIdx.items()
        self.readIdx = readIdx.items()

    def construct(self, kwargs):
        "return struct object initialized with kwargs..."

        return self.make_struct(**kwargs)

    def construct_processing_inner_fields(self, kwargs):
        "return struct object initialized with kwargs..."

        kwargs = kwargs.copy()

        # construct inner struct
        for fld, factory in self.constructIdx:
            kwargs[fld] = factory(kwargs[fld])

        return self.make_struct(**kwargs)

    def prepare(self, datas):
        "apply additional transformations to datas dictionary..."

        for fld, prepfunc in self.prepareIdx:
            datas[fld] = prepfunc(datas[fld])

        return datas

    def todict(self, msgObj):
        "dictify msgObj"

        rv = {}
        for aname, rfunc in self.readIdx:
            rv[aname] = rfunc(getattr(msgObj,aname))
        return rv

class DictProxy(StructProxy):
    """
    StructProxy in which inner Struct class is a dict
    This is to ease comparing schemaless frameworks with idl ones
    """
    
    def construct_processing_inner_fields(self, kwargs):
        "return struct object initialized with kwargs..."
        
        return self.make_struct(**kwargs)

    def todict(self, msgObj):
        "we perform some unnecessary duty here to guarantee fair comparison"

        rv = {}
        for aname, rfunc in self.readIdx:
            rv[aname] = rfunc(msgObj[aname])
        return rv

class CapNpStructProxy(StructProxy):
    "provide factory delivering initialized instances of CapNp struct"

    def __init__(self, structClass, benchargs, context=None):

        # change benchargs to name compatible with capnp naming conventions
        # the hurdle is that capnp only supports CamelCase...
        fieldnames = [a.lower().replace('_','') for a in benchargs]

        super(CapNpStructProxy, self).__init__(structClass, fieldnames, context)

        # renameIdx maps name normally used for message fields in benchmark
        # to name compatible with capnp naming conventions
        self._renameIdx = dict(zip(benchargs,fieldnames))

        self.newobj = self.construct
        self.make_struct = structClass.new_message

    def prepare(self, datas):
        "return dict with key names adapted to proxied capnp struct"

        rn = self._renameIdx.get # local alias
        return {rn(k,k):v for k,v in datas.items()}

    def todict(self, msgObj):
        "pycapnp provides efficient to_dict implementation"

        return msgObj.to_dict()


# provide json version of StuffToTest schema
def get_jsonstuff_internal(module_name):
    "return json equivalent for StuffToTest schema"

    module = importlib.import_module(module_name)

    # contruct schema
    schema = SchemaContainer('module_name', module.__version__)

    context = {}

    for message, fieldnames in FNIDX:

        # json is schemaless, for now we just process dict
        structClass = dict
        
        # contruct Struct proxy object
        structProxy = DictProxy(structClass, fieldnames, context)

        # add proxy to schema
        setattr(schema, message, structProxy)

        # update context for it to hold new structProxy reference
        context[message] = structProxy

    return schema

get_jsonstuff = partial(get_jsonstuff_internal, 'json')
get_sjsonstuff = partial(get_jsonstuff_internal, 'simplejson')
get_ujsonstuff = partial(get_jsonstuff_internal, 'ujson')

# provide msgpack version of StuffToTest schema
def get_msgpackstuff():
    "return msgpack equivalent for StuffToTest schema"

    import msgpack

    # contruct schema
    schema = SchemaContainer('msgpack', version_string(msgpack.version))

    context = {}

    for message, fieldnames in FNIDX:

        # msgpack is schemaless, for now we just process dict
        structClass = dict
        
        # contruct Struct proxy object
        structProxy = DictProxy(structClass, fieldnames, context)

        # add proxy to schema
        setattr(schema, message, structProxy)

        # update context for it to hold new structProxy reference
        context[message] = structProxy

    return schema

# index protobuf version of StuffToTest schema
def get_protostuff():
    "return protoc compiled message classes for StuffToTest schema"

    import proto_2_5_0.StuffToTest_pb2 as schmod
    
    # contruct schema
    schema = SchemaContainer('protobuf', "2.5.0")

    context = {}

    for message, fieldnames in FNIDX:

        # load protobuf message class
        structClass = getattr(schmod,message)
        
        # contruct Struct proxy object
        structProxy = StructProxy(structClass, fieldnames, context)

        # add proxy to schema
        setattr(schema, message, structProxy)

        # update context for it to hold new structProxy reference
        context[message] = structProxy

    return schema

# index thrift version of StuffToTest schema
def get_thriftstuff():
    "return thrift compiled message classes for StuffToTest schema"

    import thrift_0_9_0.StuffToTest.constants as schmod
    
    # contruct schema
    schema = SchemaContainer('thrift', "0.9.0")

    context = {}

    for message, fieldnames in FNIDX:

        # load thrift Struct class
        structClass = getattr(schmod,message)
        
        # contruct Struct proxy object
        structProxy = StructProxy(structClass, fieldnames, context)

        # add proxy to schema
        setattr(schema, message, structProxy)

        # update context for it to hold new structProxy reference
        context[message] = structProxy

    return schema

# index capnp version of StuffToTest schema
def get_pycapnpstuff():
    "return capnp adapted message factories for StuffToTest schema"

    # loads the StuffToTest schema
    import capnp
    capnp.remove_import_hook()
    schmod = capnp.load(join(PROJECT_ROOT,'idl/StuffToTest.capnp'))

    # contruct schema
    schema = SchemaContainer('pycapnp', capnp.__version__)

    context = {}

    for message, fieldnames in FNIDX:

        # load capnp Struct class
        structClass = getattr(schmod,message)
        
        # contruct Struct proxy object
        structProxy = CapNpStructProxy(structClass, fieldnames, context)

        # add proxy to schema
        setattr(schema, message, structProxy)

        # update context for it to hold new structProxy reference
        context[message] = structProxy

    return schema
