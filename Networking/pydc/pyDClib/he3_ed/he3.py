# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import struct
from codec import *

class He3Encoder:
  def __init__(self):
      pass 

  def encode(self, data):
    e = Encoder()
    e.encode(data)
    return e.encoded()

class He3Decoder:
  def __init__(self):
        pass

  def decode(self, path):
    f = open(path, 'rb')

    d = Decoder()
    if not d.decode(f.read()): raise He3FormatError
    f.close()
    return d.decoded()

class He3FormatError(Exception): pass
