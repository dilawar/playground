# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _codec
def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class BitStream(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, BitStream, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, BitStream, name)
    def __init__(self,*args):
        self.this = apply(_codec.new_BitStream,args)
        self.thisown = 1
    def getBit(*args): return apply(_codec.BitStream_getBit,args)
    def getBits(*args): return apply(_codec.BitStream_getBits,args)
    def setBit(*args): return apply(_codec.BitStream_setBit,args)
    def setBits(*args): return apply(_codec.BitStream_setBits,args)
    def pad(*args): return apply(_codec.BitStream_pad,args)
    def getByteNum(*args): return apply(_codec.BitStream_getByteNum,args)
    def __del__(self, destroy= _codec.delete_BitStream):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C BitStream instance at %s>" % (self.this,)

class BitStreamPtr(BitStream):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = BitStream
_codec.BitStream_swigregister(BitStreamPtr)

class Encoder(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Encoder, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Encoder, name)
    def __init__(self,*args):
        self.this = apply(_codec.new_Encoder,args)
        self.thisown = 1
    def __del__(self, destroy= _codec.delete_Encoder):
        try:
            if self.thisown: destroy(self)
        except: pass
    def encode(*args): return apply(_codec.Encoder_encode,args)
    def encoded(*args): return apply(_codec.Encoder_encoded,args)
    def length(*args): return apply(_codec.Encoder_length,args)
    def __repr__(self):
        return "<C Encoder instance at %s>" % (self.this,)

class EncoderPtr(Encoder):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = Encoder
_codec.Encoder_swigregister(EncoderPtr)

class Decoder(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Decoder, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Decoder, name)
    def __init__(self,*args):
        self.this = apply(_codec.new_Decoder,args)
        self.thisown = 1
    def __del__(self, destroy= _codec.delete_Decoder):
        try:
            if self.thisown: destroy(self)
        except: pass
    def decode(*args): return apply(_codec.Decoder_decode,args)
    def decoded(*args): return apply(_codec.Decoder_decoded,args)
    def __repr__(self):
        return "<C Decoder instance at %s>" % (self.this,)

class DecoderPtr(Decoder):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = Decoder
_codec.Decoder_swigregister(DecoderPtr)

class IndexError(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IndexError, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IndexError, name)
    def __init__(self,*args):
        self.this = apply(_codec.new_IndexError,args)
        self.thisown = 1
    def __del__(self, destroy= _codec.delete_IndexError):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C IndexError instance at %s>" % (self.this,)

class IndexErrorPtr(IndexError):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = IndexError
_codec.IndexError_swigregister(IndexErrorPtr)

class CompressionError(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CompressionError, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CompressionError, name)
    def __init__(self,*args):
        self.this = apply(_codec.new_CompressionError,args)
        self.thisown = 1
    def __del__(self, destroy= _codec.delete_CompressionError):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __repr__(self):
        return "<C CompressionError instance at %s>" % (self.this,)

class CompressionErrorPtr(CompressionError):
    def __init__(self,this):
        self.this = this
        if not hasattr(self,"thisown"): self.thisown = 0
        self.__class__ = CompressionError
_codec.CompressionError_swigregister(CompressionErrorPtr)


