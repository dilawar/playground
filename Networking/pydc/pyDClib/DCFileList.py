# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

class DCFileList(object):
	LIMIT_NONE = 0
	LIMIT_ATLEAST = 1
	LIMIT_ATMOST = 2

	def __init__(self):
		self._list = []
		
	def search(self, pattern, limit = LIMIT_NONE, size = 0):
		subpat = pattern.lower().split(' ')

		res = []
		for i in self._list:
			for r in self._search(i, subpat):
				res.append(r)

		return res

	def getList(self):
		return self._list
		
	###################
	# Private methods #
	###################

	def _search(self, item, subpat):
		norm = item.name.lower()

		unmatched = []
		for p in subpat:
			if norm.find(p) == -1:
				unmatched.append(p)

		res = []
		if len(unmatched) == 0 and isinstance(item, UserFile):
			res.append(item)

		if isinstance(item, UserDir):
			for i in item.children:
				for r in self._search(i, unmatched):
					res.append(r)

		return res

	list = property(getList, None, None, None)
	
class UserDir:
	def __init__(self, name, parent, children):
		self.name = name
		self.parent = parent
		self.children = children

	def getChildren(self):
		return self.children

	c = property(getChildren, None, None, None)

class UserFile:
	def __init__(self, name, parent, size):
		self.name = name
		self.parent = parent
		self.size = size
		
	def getPath(self):
		path = self.name

		item = self.parent
		while item.__class__ == UserDir:
			path = item.name + '\\' + path
			item = item.parent

		return path
		
	def fullInfo(self):
		path = self.name

		item = self.parent
		while item.__class__ == UserDir:
			path = item.name + '\\' + path
			item = item.parent

		return item.user, path, self.size

	def __str__(self):
		res  = "=========\n"
		res += "Name:" + self.name + "\n"
		res += "Size: " + str(self.size)
		return res

	path = property(getPath, None, None, None)
