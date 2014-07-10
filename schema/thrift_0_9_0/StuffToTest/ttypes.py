#
# Autogenerated by Thrift Compiler (0.9.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style,utf8strings
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Enum4(object):
  VAL_0 = 0
  VAL_1 = 1
  VAL_2 = 2
  VAL_3 = 3

  _VALUES_TO_NAMES = {
    0: "VAL_0",
    1: "VAL_1",
    2: "VAL_2",
    3: "VAL_3",
  }

  _NAMES_TO_VALUES = {
    "VAL_0": 0,
    "VAL_1": 1,
    "VAL_2": 2,
    "VAL_3": 3,
  }

class Enum16(object):
  VAL_4 = 4
  VAL_5 = 5
  VAL_6 = 6
  VAL_7 = 7
  VAL_8 = 8
  VAL_9 = 9
  VAL_10 = 10
  VAL_11 = 11
  VAL_12 = 12
  VAL_13 = 13
  VAL_14 = 14
  VAL_15 = 15
  VAL_16 = 16
  VAL_17 = 17
  VAL_18 = 18
  VAL_19 = 19

  _VALUES_TO_NAMES = {
    4: "VAL_4",
    5: "VAL_5",
    6: "VAL_6",
    7: "VAL_7",
    8: "VAL_8",
    9: "VAL_9",
    10: "VAL_10",
    11: "VAL_11",
    12: "VAL_12",
    13: "VAL_13",
    14: "VAL_14",
    15: "VAL_15",
    16: "VAL_16",
    17: "VAL_17",
    18: "VAL_18",
    19: "VAL_19",
  }

  _NAMES_TO_VALUES = {
    "VAL_4": 4,
    "VAL_5": 5,
    "VAL_6": 6,
    "VAL_7": 7,
    "VAL_8": 8,
    "VAL_9": 9,
    "VAL_10": 10,
    "VAL_11": 11,
    "VAL_12": 12,
    "VAL_13": 13,
    "VAL_14": 14,
    "VAL_15": 15,
    "VAL_16": 16,
    "VAL_17": 17,
    "VAL_18": 18,
    "VAL_19": 19,
  }


class NumStuff(object):
  """
  Attributes:
   - i01
   - i02
   - d03
   - e_04
   - l1_i05
   - l1_d06
   - l1_e07
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'i01', None, None, ), # 1
    (2, TType.I64, 'i02', None, None, ), # 2
    (3, TType.DOUBLE, 'd03', None, None, ), # 3
    (4, TType.I32, 'e_04', None, None, ), # 4
    (5, TType.LIST, 'l1_i05', (TType.I64,None), None, ), # 5
    (6, TType.LIST, 'l1_d06', (TType.DOUBLE,None), None, ), # 6
    (7, TType.LIST, 'l1_e07', (TType.I32,None), None, ), # 7
  )

  def __init__(self, i01=None, i02=None, d03=None, e_04=None, l1_i05=None, l1_d06=None, l1_e07=None,):
    self.i01 = i01
    self.i02 = i02
    self.d03 = d03
    self.e_04 = e_04
    self.l1_i05 = l1_i05
    self.l1_d06 = l1_d06
    self.l1_e07 = l1_e07

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.i01 = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I64:
          self.i02 = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.DOUBLE:
          self.d03 = iprot.readDouble();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I32:
          self.e_04 = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.LIST:
          self.l1_i05 = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = iprot.readI64();
            self.l1_i05.append(_elem5)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.LIST:
          self.l1_d06 = []
          (_etype9, _size6) = iprot.readListBegin()
          for _i10 in xrange(_size6):
            _elem11 = iprot.readDouble();
            self.l1_d06.append(_elem11)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.LIST:
          self.l1_e07 = []
          (_etype15, _size12) = iprot.readListBegin()
          for _i16 in xrange(_size12):
            _elem17 = iprot.readI32();
            self.l1_e07.append(_elem17)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('NumStuff')
    if self.i01 is not None:
      oprot.writeFieldBegin('i01', TType.I32, 1)
      oprot.writeI32(self.i01)
      oprot.writeFieldEnd()
    if self.i02 is not None:
      oprot.writeFieldBegin('i02', TType.I64, 2)
      oprot.writeI64(self.i02)
      oprot.writeFieldEnd()
    if self.d03 is not None:
      oprot.writeFieldBegin('d03', TType.DOUBLE, 3)
      oprot.writeDouble(self.d03)
      oprot.writeFieldEnd()
    if self.e_04 is not None:
      oprot.writeFieldBegin('e_04', TType.I32, 4)
      oprot.writeI32(self.e_04)
      oprot.writeFieldEnd()
    if self.l1_i05 is not None:
      oprot.writeFieldBegin('l1_i05', TType.LIST, 5)
      oprot.writeListBegin(TType.I64, len(self.l1_i05))
      for iter18 in self.l1_i05:
        oprot.writeI64(iter18)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l1_d06 is not None:
      oprot.writeFieldBegin('l1_d06', TType.LIST, 6)
      oprot.writeListBegin(TType.DOUBLE, len(self.l1_d06))
      for iter19 in self.l1_d06:
        oprot.writeDouble(iter19)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l1_e07 is not None:
      oprot.writeFieldBegin('l1_e07', TType.LIST, 7)
      oprot.writeListBegin(TType.I32, len(self.l1_e07))
      for iter20 in self.l1_e07:
        oprot.writeI32(iter20)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class StringStuff(object):
  """
  Attributes:
   - s01
   - b02
   - l1_s03
   - l1_b04
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 's01', None, None, ), # 1
    (2, TType.STRING, 'b02', None, None, ), # 2
    (3, TType.LIST, 'l1_s03', (TType.STRING,None), None, ), # 3
    (4, TType.LIST, 'l1_b04', (TType.STRING,None), None, ), # 4
  )

  def __init__(self, s01=None, b02=None, l1_s03=None, l1_b04=None,):
    self.s01 = s01
    self.b02 = b02
    self.l1_s03 = l1_s03
    self.l1_b04 = l1_b04

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.s01 = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.b02 = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.LIST:
          self.l1_s03 = []
          (_etype24, _size21) = iprot.readListBegin()
          for _i25 in xrange(_size21):
            _elem26 = iprot.readString().decode('utf-8')
            self.l1_s03.append(_elem26)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.LIST:
          self.l1_b04 = []
          (_etype30, _size27) = iprot.readListBegin()
          for _i31 in xrange(_size27):
            _elem32 = iprot.readString();
            self.l1_b04.append(_elem32)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('StringStuff')
    if self.s01 is not None:
      oprot.writeFieldBegin('s01', TType.STRING, 1)
      oprot.writeString(self.s01.encode('utf-8'))
      oprot.writeFieldEnd()
    if self.b02 is not None:
      oprot.writeFieldBegin('b02', TType.STRING, 2)
      oprot.writeString(self.b02)
      oprot.writeFieldEnd()
    if self.l1_s03 is not None:
      oprot.writeFieldBegin('l1_s03', TType.LIST, 3)
      oprot.writeListBegin(TType.STRING, len(self.l1_s03))
      for iter33 in self.l1_s03:
        oprot.writeString(iter33.encode('utf-8'))
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l1_b04 is not None:
      oprot.writeFieldBegin('l1_b04', TType.LIST, 4)
      oprot.writeListBegin(TType.STRING, len(self.l1_b04))
      for iter34 in self.l1_b04:
        oprot.writeString(iter34)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ComboStuff(object):
  """
  Attributes:
   - i01
   - i02
   - d03
   - e_04
   - l1_i05
   - l1_d06
   - l1_e07
   - s08
   - b09
   - l1_s10
   - l1_b11
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'i01', None, None, ), # 1
    (2, TType.I64, 'i02', None, None, ), # 2
    (3, TType.DOUBLE, 'd03', None, None, ), # 3
    (4, TType.I32, 'e_04', None, None, ), # 4
    (5, TType.LIST, 'l1_i05', (TType.I64,None), None, ), # 5
    (6, TType.LIST, 'l1_d06', (TType.DOUBLE,None), None, ), # 6
    (7, TType.LIST, 'l1_e07', (TType.I32,None), None, ), # 7
    (8, TType.STRING, 's08', None, None, ), # 8
    (9, TType.STRING, 'b09', None, None, ), # 9
    (10, TType.LIST, 'l1_s10', (TType.STRING,None), None, ), # 10
    (11, TType.LIST, 'l1_b11', (TType.STRING,None), None, ), # 11
  )

  def __init__(self, i01=None, i02=None, d03=None, e_04=None, l1_i05=None, l1_d06=None, l1_e07=None, s08=None, b09=None, l1_s10=None, l1_b11=None,):
    self.i01 = i01
    self.i02 = i02
    self.d03 = d03
    self.e_04 = e_04
    self.l1_i05 = l1_i05
    self.l1_d06 = l1_d06
    self.l1_e07 = l1_e07
    self.s08 = s08
    self.b09 = b09
    self.l1_s10 = l1_s10
    self.l1_b11 = l1_b11

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.i01 = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I64:
          self.i02 = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.DOUBLE:
          self.d03 = iprot.readDouble();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I32:
          self.e_04 = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.LIST:
          self.l1_i05 = []
          (_etype38, _size35) = iprot.readListBegin()
          for _i39 in xrange(_size35):
            _elem40 = iprot.readI64();
            self.l1_i05.append(_elem40)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.LIST:
          self.l1_d06 = []
          (_etype44, _size41) = iprot.readListBegin()
          for _i45 in xrange(_size41):
            _elem46 = iprot.readDouble();
            self.l1_d06.append(_elem46)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.LIST:
          self.l1_e07 = []
          (_etype50, _size47) = iprot.readListBegin()
          for _i51 in xrange(_size47):
            _elem52 = iprot.readI32();
            self.l1_e07.append(_elem52)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.STRING:
          self.s08 = iprot.readString().decode('utf-8')
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.STRING:
          self.b09 = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 10:
        if ftype == TType.LIST:
          self.l1_s10 = []
          (_etype56, _size53) = iprot.readListBegin()
          for _i57 in xrange(_size53):
            _elem58 = iprot.readString().decode('utf-8')
            self.l1_s10.append(_elem58)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 11:
        if ftype == TType.LIST:
          self.l1_b11 = []
          (_etype62, _size59) = iprot.readListBegin()
          for _i63 in xrange(_size59):
            _elem64 = iprot.readString();
            self.l1_b11.append(_elem64)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ComboStuff')
    if self.i01 is not None:
      oprot.writeFieldBegin('i01', TType.I32, 1)
      oprot.writeI32(self.i01)
      oprot.writeFieldEnd()
    if self.i02 is not None:
      oprot.writeFieldBegin('i02', TType.I64, 2)
      oprot.writeI64(self.i02)
      oprot.writeFieldEnd()
    if self.d03 is not None:
      oprot.writeFieldBegin('d03', TType.DOUBLE, 3)
      oprot.writeDouble(self.d03)
      oprot.writeFieldEnd()
    if self.e_04 is not None:
      oprot.writeFieldBegin('e_04', TType.I32, 4)
      oprot.writeI32(self.e_04)
      oprot.writeFieldEnd()
    if self.l1_i05 is not None:
      oprot.writeFieldBegin('l1_i05', TType.LIST, 5)
      oprot.writeListBegin(TType.I64, len(self.l1_i05))
      for iter65 in self.l1_i05:
        oprot.writeI64(iter65)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l1_d06 is not None:
      oprot.writeFieldBegin('l1_d06', TType.LIST, 6)
      oprot.writeListBegin(TType.DOUBLE, len(self.l1_d06))
      for iter66 in self.l1_d06:
        oprot.writeDouble(iter66)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l1_e07 is not None:
      oprot.writeFieldBegin('l1_e07', TType.LIST, 7)
      oprot.writeListBegin(TType.I32, len(self.l1_e07))
      for iter67 in self.l1_e07:
        oprot.writeI32(iter67)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.s08 is not None:
      oprot.writeFieldBegin('s08', TType.STRING, 8)
      oprot.writeString(self.s08.encode('utf-8'))
      oprot.writeFieldEnd()
    if self.b09 is not None:
      oprot.writeFieldBegin('b09', TType.STRING, 9)
      oprot.writeString(self.b09)
      oprot.writeFieldEnd()
    if self.l1_s10 is not None:
      oprot.writeFieldBegin('l1_s10', TType.LIST, 10)
      oprot.writeListBegin(TType.STRING, len(self.l1_s10))
      for iter68 in self.l1_s10:
        oprot.writeString(iter68.encode('utf-8'))
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l1_b11 is not None:
      oprot.writeFieldBegin('l1_b11', TType.LIST, 11)
      oprot.writeListBegin(TType.STRING, len(self.l1_b11))
      for iter69 in self.l1_b11:
        oprot.writeString(iter69)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class ComboBunch(object):
  """
  Attributes:
   - e_01
   - ns02
   - ss03
   - cs04
   - l2_ns05
   - l2_ss06
   - l2_cs07
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'e_01', None, None, ), # 1
    (2, TType.STRUCT, 'ns02', (NumStuff, NumStuff.thrift_spec), None, ), # 2
    (3, TType.STRUCT, 'ss03', (StringStuff, StringStuff.thrift_spec), None, ), # 3
    (4, TType.STRUCT, 'cs04', (ComboStuff, ComboStuff.thrift_spec), None, ), # 4
    (5, TType.LIST, 'l2_ns05', (TType.STRUCT,(NumStuff, NumStuff.thrift_spec)), None, ), # 5
    (6, TType.LIST, 'l2_ss06', (TType.STRUCT,(StringStuff, StringStuff.thrift_spec)), None, ), # 6
    (7, TType.LIST, 'l2_cs07', (TType.STRUCT,(ComboStuff, ComboStuff.thrift_spec)), None, ), # 7
  )

  def __init__(self, e_01=None, ns02=None, ss03=None, cs04=None, l2_ns05=None, l2_ss06=None, l2_cs07=None,):
    self.e_01 = e_01
    self.ns02 = ns02
    self.ss03 = ss03
    self.cs04 = cs04
    self.l2_ns05 = l2_ns05
    self.l2_ss06 = l2_ss06
    self.l2_cs07 = l2_cs07

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.I32:
          self.e_01 = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRUCT:
          self.ns02 = NumStuff()
          self.ns02.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRUCT:
          self.ss03 = StringStuff()
          self.ss03.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRUCT:
          self.cs04 = ComboStuff()
          self.cs04.read(iprot)
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.LIST:
          self.l2_ns05 = []
          (_etype73, _size70) = iprot.readListBegin()
          for _i74 in xrange(_size70):
            _elem75 = NumStuff()
            _elem75.read(iprot)
            self.l2_ns05.append(_elem75)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.LIST:
          self.l2_ss06 = []
          (_etype79, _size76) = iprot.readListBegin()
          for _i80 in xrange(_size76):
            _elem81 = StringStuff()
            _elem81.read(iprot)
            self.l2_ss06.append(_elem81)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.LIST:
          self.l2_cs07 = []
          (_etype85, _size82) = iprot.readListBegin()
          for _i86 in xrange(_size82):
            _elem87 = ComboStuff()
            _elem87.read(iprot)
            self.l2_cs07.append(_elem87)
          iprot.readListEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('ComboBunch')
    if self.e_01 is not None:
      oprot.writeFieldBegin('e_01', TType.I32, 1)
      oprot.writeI32(self.e_01)
      oprot.writeFieldEnd()
    if self.ns02 is not None:
      oprot.writeFieldBegin('ns02', TType.STRUCT, 2)
      self.ns02.write(oprot)
      oprot.writeFieldEnd()
    if self.ss03 is not None:
      oprot.writeFieldBegin('ss03', TType.STRUCT, 3)
      self.ss03.write(oprot)
      oprot.writeFieldEnd()
    if self.cs04 is not None:
      oprot.writeFieldBegin('cs04', TType.STRUCT, 4)
      self.cs04.write(oprot)
      oprot.writeFieldEnd()
    if self.l2_ns05 is not None:
      oprot.writeFieldBegin('l2_ns05', TType.LIST, 5)
      oprot.writeListBegin(TType.STRUCT, len(self.l2_ns05))
      for iter88 in self.l2_ns05:
        iter88.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l2_ss06 is not None:
      oprot.writeFieldBegin('l2_ss06', TType.LIST, 6)
      oprot.writeListBegin(TType.STRUCT, len(self.l2_ss06))
      for iter89 in self.l2_ss06:
        iter89.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    if self.l2_cs07 is not None:
      oprot.writeFieldBegin('l2_cs07', TType.LIST, 7)
      oprot.writeListBegin(TType.STRUCT, len(self.l2_cs07))
      for iter90 in self.l2_cs07:
        iter90.write(oprot)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
