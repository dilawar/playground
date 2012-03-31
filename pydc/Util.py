# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import gc
import sys
from wxPython.wx import *

def getMainWnd():
	return sys.modules["__main__"].wnd

def partialSort(items, access, comp, item):
	num = len(items)
	if len(items) == 1: return (0, 0, items)

	oldPos = items.index(item)
	del items[oldPos]
	num -= 1

	pos = oldPos
	if oldPos == num: pos -= 1

	value = apply(access, (item,))
	if pos == 0:
		direction = 1
	elif pos == num-1:
		direction = -1
	else:
		cval = apply(access, (items[pos],))
		res = apply(comp, (value, cval))
		if res > 0:
			direction = 1
		elif res < 0:
			direction = -1
		else:
			items = items[:pos] + [item] + items[pos:]
			return (oldPos, pos, items)

	if direction == 1:
		while pos < num:
			cval = apply(access, (items[pos],))
			res = apply(comp, (value, cval))
			if res <= 0:
				pos = max(0, pos-1)
				items = items[:pos] + [item] + items[pos:]
				return (oldPos, pos, items)
			else:
				pos += 1
	elif direction == -1:
		while pos >= 0:
			cval = apply(access, (items[pos],))
			res = apply(comp, (cval, value))
			if res <= 0:
				pos = min(num, pos+1)
				items = items[:pos] + [item] + items[pos:]
				return (oldPos, pos, items)
			else:
				pos -= 1
		pos = 0

	items = items[:pos] + [item] + items[pos:]
	return (oldPos, pos, items)

def fullSort(items, access, comp):
	aux = []
	for item in items:
		aux.append( (apply(access, (item,)), item) )
	aux.sort(comp)

	items = []
	for item in aux:
		items.append(item[1])
	return items

def icmp(x, y):
	return -cmp(x,y)

def basename(path):
	try:
		return path[path.rindex('\\')+1:]
	except ValueError:
		return path

def formatSize(size):
	try:
		if size < 1024: return '%d b' % size

		size /= 1024.0
		if size < 1024: return '%.2f kb' % size

		size /= 1024
		if size < 1024: return '%.2f MB' % size

		size /= 1024
		if size < 1024: return '%.2f GB' % size

		size /= 1024
		return '%.2f TB' % size
	except OverflowError:
		return 'too large'
	
def formatSpeed(speed):
	if speed < 1024: return '%d b/s' % speed
	
	speed /= 1024.0
	if speed < 1024: return '%.2f kb/s' % speed

	speed /= 1024
	return '%.2f MB/s' % speed

class guiEvent(wxPyEvent):
	def __init__(self, id, data):
		wxPyEvent.__init__(self, id)
		self.data = data
