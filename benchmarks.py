# -*- coding: utf-8 -*-
"""
    benchmarks
    ~~~~~~~~~~

    Classes that allows to benchmark serialization/deserialization of objects
    defined in StuffToTest schema... 

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""
__version__ = (1,0,0)

from random import Random
from struct import Struct
from array import array

unpack_double = Struct('=d').unpack

from utils import *

FRAMEWORKS = [
        ('protobuf','py'), ('protobuf','pyext'),
        ('thrift','py'), ('thrift','pyext')
        ]

BENCHMARK_MESSAGES = ['NumStuff', 'StringStuff', 'ComboStuff', 'ComboBunch']

class StuffToTestRandom(Random):
    """Custom Random generator that ease the generation of StuffToTest messages"""

    _ucs2Range = (0, 0xffff)

    _ucs2Range = (0, 127)

    _i32Range = (-2**31, 2**31-1)

    _i64Range = (-2**63, 2**63-1)

    def __new__(cls, srange, l1range, l2range, seed=None):

        return Random.__new__(cls, seed)

    def __init__(self, srange, l1range, l2range, seed=None):

        self.srange = srange

        self.l1range = l1range
        
        self.l2range = l2range

    def rande4(self):
        """ return integer in range [0,3] """

        return self.randint(0, 3)

    def rande16(self):
        """" return integer in range [4,19] """

        return self.randint(4, 19)

    def randbyte(self):
        """return integer in range [0,255]"""

        return self.randint(0, 255)

    def randbinary(self):
        """return random binary string"""

        size = self.choice(self.srange)
        rb = self.randbyte  # local alias
        ba = array('B', [rb() for i in xrange(size)])
        return ba.tostring()

    def randunichr(self):
        """ return random unicode character in UCS2 range"""

        return unichr(self.randint(*self._ucs2Range))

    def randunicode(self, sizerange=64):
        """return random unicode string with size in sizerange"""

        size = self.choice(self.srange)
        rc = self.randunichr  # local alias
        uca = array('u', [rc() for i in xrange(size)])
        return uca.tounicode()

    def randi32(self):
        """return random i32"""

        return self.randint(*self._i32Range)

    def randi64(self):
        """return random i64"""
        
        return self.randint(*self._i64Range)

    def randdouble(self):
        """return random double"""

        rb = self.randbyte  # local alias
        b8 = array('B', [rb() for i in xrange(8)]).tostring()
        return unpack_double(b8)[0]

    def gen_numstuff(self, ProtoOrThrift):
        """return random NumStuff datas..."""

        l1range = self.l1range  # local alias

        rv = {}

        rv['i01'] = self.randi32()
        
        rv['i02'] = self.randi64()
        
        rv['d03'] = self.randdouble()
        
        rv['e_04'] = self.rande4()

        l1 = self.choice(l1range)
        rv['l1_i05'] = [self.randi64() for i in xrange(l1)]
        
        l1 = self.choice(l1range)
        rv['l1_d06'] = [self.randdouble() for i in xrange(l1)]

        l1 = self.choice(l1range)
        rv['l1_e07'] = [self.rande16() for i in xrange(l1)]

        return ProtoOrThrift.NumStuff(**rv)

    def gen_stringstuff(self, ProtoOrThrift):
        """return random StringStuff datas..."""

        l1range = self.l1range # local alias

        rv = {}

        rv['s01'] = self.randunicode()

        rv['b02'] = self.randbinary()

        l1 = self.choice(l1range)
        rv['l1_s03'] = [self.randunicode() for i in xrange(l1)]
        
        l1 = self.choice(l1range)
        rv['l1_b04'] = [self.randbinary() for i in xrange(l1)]

        return ProtoOrThrift.StringStuff(**rv)

    def gen_combostuff(self, ProtoOrThrift):
        """return random ComboStuff datas..."""

        l1range = self.l1range  # local alias

        rv = {}

        rv['i01'] = self.randi32()
        
        rv['i02'] = self.randi64()
        
        rv['d03'] = self.randdouble()
        
        rv['e_04'] = self.rande4()

        l1 = self.choice(l1range)
        rv['l1_i05'] = [self.randi64() for i in xrange(l1)]
        
        l1 = self.choice(l1range)
        rv['l1_d06'] = [self.randdouble() for i in xrange(l1)]

        l1 = self.choice(l1range)
        rv['l1_e07'] = [self.rande16() for i in xrange(l1)]

        rv['s08'] = self.randunicode()

        rv['b09'] = self.randbinary()

        l1 = self.choice(l1range)
        rv['l1_s10'] = [self.randunicode() for i in xrange(l1)]
        
        l1 = self.choice(l1range)
        rv['l1_b11'] = [self.randbinary() for i in xrange(l1)]

        return ProtoOrThrift.ComboStuff(**rv)

    def gen_combobunch(self, ProtoOrThrift):
        """return random ComboBunch datas"""
        
        # local alias
        l2range = self.l2range

        rv = {}

        rv['e_01'] = self.rande16()

        rv['ns02'] = self.gen_numstuff(ProtoOrThrift)

        rv['ss03'] = self.gen_stringstuff(ProtoOrThrift)

        rv['cs04'] = self.gen_combostuff(ProtoOrThrift)

        l2 = self.choice(l2range)
        rv['l2_ns05'] = [self.gen_numstuff(ProtoOrThrift) for i in xrange(l2)]

        l2 = self.choice(l2range)
        rv['l2_ss06'] = [self.gen_stringstuff(ProtoOrThrift) for i in xrange(l2)]

        l2 = self.choice(l2range)
        rv['l2_cs07'] = [self.gen_combostuff(ProtoOrThrift) for i in xrange(l2)]

        return ProtoOrThrift.ComboBunch(**rv)


class Benchmark(object):

    def __init__(self, schema,
            serialize_func, deserialize_func=None,
            seed=None, ns=128, bs=64, l1=4, l2=32
            ):

        # set schema
        for sname in ['NumStuff','StringStuff','ComboStuff','ComboBunch']:
            if not hasattr(schema,sname):
                raise ValueError("Invalid schema!")
        self.schema = schema

        # set serialize
        if not callable(serialize_func):
            raise ValueError("Invalid serialize function!")
        self.serialize = serialize_func

        # set deserialize
        if deserialize_func is not None:

            if not callable(deserialize_func):
                raise ValueError("Invalid deserialize function!")

            self.deserialize = deserialize_func
            target = 'deserialize'

        else:

            self.deserialize = None
            target = 'serialize'

        # control number of samples in benchmark...
        ns = int(ns)
        if ns <= 0:
            raise ValueError("Invalid ns, can not be <= 0 !")
        self.ns = ns

        # control size of fields of type string and binary...
        bs = int(bs)
        if bs <= 0:
            raise ValueError("Invalid bs, can not be <= 0 !")
        bsrange = range(bs, 2*bs, 1)

        # control size of repetition of type l1...
        l1 = int(l1)
        if l1 < 0:
            raise ValueError("Invalid l1, can not be < 0 !")
        l1range = range(l1, 2*l1, 1)

        # control size of repetition of type l2...
        l2 = int(l2)
        if l2 < 0:
            raise ValueError("Invalid l2, can not be < 0 !")
        l2range = range(l2, 2*l2, 1)

        # set benchmark random number generator
        self.seed = (seed, bs, l1, l2)
        self.rnd = StuffToTestRandom(bsrange, l1range, l2range, self.seed)
        
        # prepare the benchmark

        prepmeth = "prepare_%s" % target
        getattr(self, prepmeth)()

        runmeth = "run_%s" % target
        self.run = getattr(self, runmeth)

    def gen_message_datas(self):
        """return dict containing message datas"""

        raise NotImplemented("gen_message_datas not implemented !")

    def gen_benchmark_sample(self):

        # seed random number generation
        self.rnd.seed(self.seed)

        return [self.gen_message_datas() for i in xrange(self.ns)]

    def prepare_serialize(self):

        self.sample = self.gen_benchmark_sample()

    def run_serialize(self):

        map(self.serialize, self.sample)

    def prepare_deserialize(self):

        srz = self.serialize
        self.sample = [srz(m) for m in self.gen_benchmark_sample()]

    def run_deserialize(self):

        map(self.deserialize, self.sample)

class NumStuffBenchmark(Benchmark):

    def gen_message_datas(self):

        return self.rnd.gen_numstuff(self.schema)

class StringStuffBenchmark(Benchmark):

    def gen_message_datas(self):

        return self.rnd.gen_stringstuff(self.schema)

class ComboStuffBenchmark(Benchmark):

    def gen_message_datas(self):

        return self.rnd.gen_combostuff(self.schema)

class ComboBunchBenchmark(Benchmark):

    def gen_message_datas(self):

        return self.rnd.gen_combobunch(self.schema)

def build_benchmark(message, framework, implementation, target, **benchargs):
    "return ready to run benchmark"

    use_extension = implementation.startswith('pyext')

    # Validate framework
    if (framework,implementation) not in FRAMEWORKS:
        raise ValueError("Invalid (framework,implementation)!")

    if framework == 'protobuf':

        # Set environment variables 
        # necessary to control protobuf framework implementation
        import os
        if use_extension:
            os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'cpp'
        else:
            os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

        # Validate that framework can be loaded 
        if not is_protobuf_available(use_extension):
            raise RuntimeError("required framework can not be loaded !")

        # load schema
        from schema import get_protostuff
        benchargs['schema'] = get_protostuff()

        # add serializer
        benchargs['serialize_func'] = build_protobuf_serializer()

        build_dsrz = build_protobuf_deserializer

    elif framework == 'thrift':

        # Validate that framework can be loaded 
        if not is_thrift_available(use_extension):
            raise RuntimeError("required framework can not be loaded !")
    
        # load schema
        from schema import get_thriftstuff
        benchargs['schema'] = get_thriftstuff()

        # add serializer
        benchargs['serialize_func'] = build_thrift_serializer(use_extension)
    
        build_dsrz = build_thrift_deserializer
    
    else:

        # shall not happen
        raise RuntimeError("missing framework initializer !")

    # make sure that message is part of StuffToTest schema...
    if message not in BENCHMARK_MESSAGES:
        raise ValueError("Invalid message !")

    # load the required Benchmark class
    bname = "%sBenchmark" % message
    BenchClass = globals()[bname]

    # validate target
    if target not in ['serialize', 'deserialize']:
        raise ValueError("Invalid target !")

    # add deserialize_func
    if target == 'deserialize':

        MsgClass = getattr(benchargs['schema'], message)
        benchargs['deserialize_func'] = build_dsrz(MsgClass, use_extension)

    # prepare the Benchmark
    benchmark = BenchClass(**benchargs)

    return benchmark
