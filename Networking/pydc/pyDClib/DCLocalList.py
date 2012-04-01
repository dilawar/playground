# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import os
import os.path
from DCFileList import *

class DCLocalList(DCFileList):
	def __init__(self, path):
		DCFileList.__init__(self)
		
		self._path = os.path.abspath(path)
		if not os.path.isdir(self._path):
			self._path = None
			raise IllegalPath

		self.scan()

	def scan(self, path = None, parent = None, l = None):
		if path == None:
			self._size = 0L

			d = UserDir(self._path[self._path.rindex(os.sep)+1:], None, [])
			self.scan(self._path, d, d.children)
			self._list = [d]
			
			return

		items = os.listdir(path)
		for i in items:
			fullname = path + os.sep + i
			if os.path.isdir(fullname):
				d = UserDir(i, parent, [])
				self.scan(fullname, d, d.children)
				l.append(d)
			else:
				size = os.stat(fullname).st_size
				l.append(UserFile(i, parent, size))
				self._size += size

	def getPath(self):
		return self._path
		
	def getSize(self):
		return self._size

	path = property(getPath, None, None, None)
	size = property(getSize, None, None, None)

class IllegalPath(Exception): pass
