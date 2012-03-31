# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from DCWorker import *
from DCSettings import ParseError
from DCHub import *
from DCSearch import *
from DCXfer import *
from DCQueueItem import *
from DCUserList import *
from HublistWaiter import *
import exceptions
import os
import os.path
import sys
import time

def initDC():
	try:
		getWorker().loadSettings('..' + os.sep + 'settings.xml')
	except LocalIPError:
		print "Unable to retrieve local IP. Try using the 'ip' field in configuration file."
		sys.exit(1)
	except ParseError, e:
		print "Got an error while reading 'settings.xml': %s." % e.description
		sys.exit(1)

	getWorker().start()
	
def getHublist():
	w = HublistWaiter()
	w.wait()
	return w.list

def l():
	return sys.modules['__main__'].hublist

def refreshHublist():
	sys.stdout.write("Retrieving hublist... ")
	sys.stdout.flush()
	sys.modules['__main__'].hublist = getHublist()
	if len(sys.modules['__main__'].hublist) == 0:
		print "FAILED"
	else:
		sys.modules['__main__'].hublist.sort(lambda x,y:y[3]-x[3])
		sys.modules['__main__'].hublist = filter(lambda x:x[3]>10, sys.modules['__main__'].hublist)
		print "SUCCESS"

def connectFromList(list, start = 0, end = -1):
	if end == -1: end = len(list)
	addrs = map(lambda x: x[1], list[start:end])

	hubs = []
	for addr in addrs:
		newHub = DCHub(addr)
		hubs.append(newHub)
		w.addJob(newHub)

	return hubs

def connectTo(hub):
	if hub.__class__ == str:
		newHub = DCHub(hub)
		getWorker().addJob(newHub)
		return newHub

	elif hub.__class__ == list:
		if len(hub) == 0: return []

		w = getWorker()
		hubs = []

		for addr in hub:
			newHub = DCHub(addr)
			hubs.append(newHub)
			w.addJob(newHub)

		return hubs

	else:
		print "Parameter not supported."
		return None

def queueItem(search, id, path=None):
	res = search.results
	if id >= len(res):
		print "ID argument is nonsense!"
		return

	try:
		getWorker().getQueue().addItem(res[id], path)
	except ItemAlreadyAddedError:
		print "The item is already queued!"

def queueFile(userFile, path=None):
	try:
		item = DCItem()
		user, item.path, item.size = userFile.fullInfo()
		item.userNick = user.nick
		getWorker().queue.addItem(item, path)
	except ItemAlreadyAddedError:
		print "The item is already queued!"
		
def queueDir(userDir, prefix=None):
	if prefix != None:
		fullPrefix = os.path.abspath(DCWorker.getWorker().getSettings().download + os.sep + prefix)
		if not os.path.isdir(fullPrefix):
			print prefix, "is not a valid directory!"
			return
	else:
		fullPrefix = DCWorker.getWorker().getSettings().download

	for i in userDir.children:
		if i.__class__ == UserDir:
			path = fullPrefix + os.sep + i.name
			if os.path.exists(path):
				if not os.path.isdir(path):
					print "I should create some files into", path, ", but it's not a directory!"
					return
			else:
				try: os.mkdir(path)
				except OSError:
					print "I tried to create", path, "directory, but where was an error!"
					return 0
			
			path = i.name
			if prefix:
				path = prefix + os.sep + path

			queueDir(i, path)
		else:
			path = i.name
			if prefix:
				path = prefix + os.sep + path

			queueFile(i, path)

def addSource(search, id, queueId):
	res = search.results
	if id >= len(res):
		print "ID argument is nonsense!"
		return

	items = getWorker().queue.items
	if queueId >= len(items):
		print "queueID argument is nonsense!"
		return

	try:
		items[queueId].addSource(res[id])
	except ItemNotMatching:
		print "New source is not matching!"
	except ExistingSourceError:
		print "The source has been already added!"

def removeSource(queueId, nick):
	items = getWorker().queue.items
	if queueId >= len(items):
		print "queueID argument is nonsense!"
		return

	items[queueId].removeSource(nick)

def dequeueItem(id):
	items = getWorker().getQueue().items
	if id >= len(items):
		print "ID argument is nonsense!"
		return

	getWorker().getQueue().removeItem(items[id])

def dequeueCompleted():
	queue = getWorker().getQueue()
	for i in getWorker().getQueue().items:
		if i.status == STATUS_COMPLETED:
			queue.removeItem(i)

def getDownloadHubs():
	hubs = []
	for item in getWorker().queue.items:
		if item.status == DCQueueItem.STATUS_COMPLETED: continue
		for source in item.sources:
			for user in getWorker().getUsersByNick(source.nick):
				hubs.append(user.hub)
	return hubs

def disconnectUnusedHubs():
	used = getDownloadHubs()
	for hub in getWorker().hubs:
		if not hub in used:
			hub.stop()

def getUserlist(nick):
	try:
		userList = DCUserList(w.getUsersByNick(nick)[0])
		w.addJob(userList)
		return userList
	except exceptions.IndexError:
		print "No such user!"

def search(query):
	s = DCSearch(query)
	s.start()
	return s

def hubs(sort = 0):
	infos = []
	for hub in getWorker().hubs:
		info = [hub.name, hub.status, hub.userNum]
		infos.append(info)

	if sort == 1:
		infos.sort(lambda x, y: cmp(x[0], y[0]))
	elif sort == 2:
		infos.sort(lambda x, y: y[1] - x[1])
	elif sort == 3:
		infos.sort(lambda x, y: y[2] - x[2])
	elif sort != 0:
		print "Sort argument is nonsense!"
		return

	print "%-50s %-10s %s" % ("Hub", "Status", "Users")

	for info in infos:
		try:
			if len(info[0]) > 30:
				info[0] = info[0][:29] + "_"
		except TypeError: info[0] = ""

		if info[1] == DCHub.STATUS_CONNECTING:
			info[1] = "connecting"
		elif info[1] == DCHub.STATUS_CONNECTED:
			info[1] = "connected"
		elif info[1] == DCHub.STATUS_CLOSED:
			info[1] = "closed"
		else:
			info[1] = "unknown"

		print "%-50s %-10s %4d" % (info[0], info[1], info[2])

def res(search, sort = 0, max = 0):
	infos = []
	id = 0
	for result in search.results:
		base = result.path[result.path.rfind('\\')+1:]
		info = [id, result.userNick, base, result.size, result.freeSlots, result.slots]

		id += 1
		infos.append(info)

	if sort == 1:
		infos.sort(lambda x, y: y[0] - x[0])
	elif sort == 2:
		infos.sort(lambda x, y: cmp(x[1], y[1]))
	elif sort == 3:
		infos.sort(lambda x, y: cmp(x[2], y[2]))
	elif sort == 4:
		infos.sort(lambda x, y: cmpLong(x[3], y[3]))
	elif sort == 5:
		infos.sort(lambda x, y: y[4] - x[4])
	elif sort != 0:
		print "Sort argument is nonsense!"
		return

	print "%-3s %-15s %-42s %10s %-5s" % ("ID", "User", "File", "Size", "Slots")

	if max != 0: infos = infos[:max]
	for info in infos:
		if len(info[1]) > 15: info[1] = info[1][:14] + "_"
		if len(info[2]) > 42: info[2] = "_" + info[2][-41:]

		print "%3s %-15s %-42s %10s %-5s" % \
				(info[0], info[1], info[2], str(info[3]), `info[4]` + "/" + `info[5]`)

def queue(sort = 0):
	infos = []
	id = 0
	for item in getWorker().queue.items:
		sources = item.sources
		if len(sources) == 1:
			nick = sources[0].nick
		elif len(sources) == 0:
			nick = "none"
		else:
			nick = "many"

		base = item.path
		info = [id, base, nick, item.size, item.status, item.progress]

		id += 1
		infos.append(info)

	if sort == 1:
		infos.sort(lambda x, y: y[0] - x[0])
	elif sort == 2:
		infos.sort(lambda x, y: cmp(x[1], y[1]))
	elif sort == 3:
		infos.sort(lambda x, y: cmp(x[2], y[2]))
	elif sort == 4:
		infos.sort(lambda x, y: cmpLong(x[3], y[3]))
	elif sort == 5:
		infos.sort(lambda x, y: y[4] - x[4])
	elif sort == 6:
		infos.sort(lambda x, y: y[5] - x[5])
	elif sort != 0:
		print "Sort argument is nonsense!"
		return

	print "%-3s %-34s %-15s %-10s %-8s %4s" % ("ID", "File", "User", "Size", "Status", "%")

	for info in infos:
		if len(info[1]) > 33: info[1] = "_" + info[1][-32:]
		if len(info[2]) > 15: info[2] = info[2][:14] + "_"

		if info[4] == DCQueueItem.STATUS_WAITING:
			status = "waiting"
		elif info[4] == DCQueueItem.STATUS_RUNNING:
			status = "running"
		elif info[4] == DCQueueItem.STATUS_COMPLETED:
			status = "complete"
		elif info[4] == DCQueueItem.STATUS_ERROR:
			status = "error"
		else:
			status = "unknown"

		print "%-3d %-34s %-15s %10s %-8s %3d%%" % \
				(info[0], info[1], info[2], str(info[3]), status, info[5])

def xfers(sort = 0):
	infos = []
	id = 0
	for xfer in getWorker().xferListener.xfers:
		if xfer.item == None: continue

		if xfer.getType() == DCXfer.TYPE_DOWNLOAD:
			type = 'D'
		else:
			type = 'U'
		base = xfer.item.path

		info = [type, id, xfer.remoteNick, base, xfer.item.size, xfer.progress]
		id += 1

		infos.append(info)

	if sort == 1:
		infos.sort(lambda x, y: y[1] - x[1])
	elif sort == 2:
		infos.sort(lambda x, y: cmp(x[2], y[2]))
	elif sort == 3:
		infos.sort(lambda x, y: cmp(x[3], y[3]))
	elif sort == 4:
		infos.sort(lambda x, y: cmpLong(x[4], y[4]))
	elif sort == 5:
		infos.sort(lambda x, y: y[5] - x[5])
	elif sort != 0:
		print "Sort argument is nonsense!"
		return

	print "  %-3s %-15s %-41s %-10s %4s" % ("ID", "User", "File", "Size", "%")

	for info in infos:
		if len(info[2]) > 15: info[2] = info[2][:14] + "_"
		if len(info[3]) > 41: info[3] = "_" + info[3][-40:]

		print "%s %-3s %-15s %-41s %10s %3d%%" % \
				(info[0], info[1], info[2], info[3], str(info[4]), info[5])

def xfersEta(sort = 0):
	infos = []
	id = 0
	for xfer in getWorker().xferListener.xfers:
		if xfer.item == None: continue
		base = xfer.item.path
		if xfer.speed > 0:
			secs = xfer.sizeRemaining / xfer.speed
		else:
			secs = 0
		info = [id, base, xfer.progress, xfer.speed, secs]

		id += 1
		infos.append(info)

	if sort == 1:
		infos.sort(lambda x, y: y[0] - x[0])
	elif sort == 2:
		infos.sort(lambda x, y: cmp(x[1], y[1]))
	elif sort == 3:
		infos.sort(lambda x, y: cmpFloat(x[2], y[2]))
	elif sort == 4:
		infos.sort(lambda x, y: y[3] - x[3])
	elif sort == 5:
		infos.sort(lambda x, y: cmp(x[4], y[4]))
	elif sort != 0:
		print "Sort argument is nonsense!"
		return

	print "%-3s %-43s %4s %-8s %-8s" % ("ID", "File", "%", "Speed", "ETA")

	for info in infos:
		if len(info[1]) > 43: info[1] = "_" + info[1][-42:]

		if info[3] < 1024:
			unit = "b"
		else:
			info[3] = info[3] / 1024
			unit = "k"
		speed = "%.2f %s" % (info[3], unit)

		print "%-3d %-43s %3d%% %8s %8s" % \
				(info[0], info[1], info[2], speed, formatTime(info[4]))
				
def printDir(userDir):
	print "%-4s %-55s %-10s" % ("ID", "Name", "(Size)")

	id = 0
	if userDir.__class__ == DCUserList:
		l = userDir.list
	elif userDir.__class__ == list:
		l = userDir
	elif userDir.__class__ == UserDir:
		l = userDir.children
	else:
		l = []

	for item in l:
		if len(item.name) > 55:
			name = '_' + item.name[:-54]
		else:
			name = item.name

		if item.__class__ == UserDir:
			print "%4d %-55s" % (id, name)
		else:
			print "%4d %-55s %10d" % (id, name, item.size)

		id += 1

def cmpLong(x, y):
	delta = y - x
	if delta > 0: return 1
	elif delta < 0: return -1
	else: return 0
	
def cmpFloat(x, y):
	delta = y - x
	if delta > 0: return 1
	elif delta < 0: return -1
	else: return 0
	
def formatTime(secs):
	part = secs % 3600
	h = (secs - part) / 3600
	secs = part

	part = secs % 60
	m = (secs - part) / 60
	secs = part
	
	return "%.2d:%.2d:%.2d" % (h, m, secs)

w = getWorker()

if __name__ == "__main__":
	initDC()
	refreshHublist()
else:
	from Util import getMainWnd
