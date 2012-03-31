# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from threading import Lock
from time import time
from Util import *
from ViewerListener import *
from wxPython.wx import *
import os.path

from DCXfer import *
from DCXferListenerEventListener import *
import DCWorker

class XfersPanel(wxPanel, ViewerListener, DCXferListenerEventListener):
	INFO_TIMEOUT = 3

	def __init__(self, parent, id):
		wxPanel.__init__(self, parent, id)

		self.xfers = []
		self.lock = Lock()
		self.sortAlgos = [ None,
		                   (DCXfer.getType, icmp),
		                   (self.getXferPath, cmp),
		                   (self.getXferProgress, icmp),
		                   (DCXfer.getSpeed, icmp),
		                   (self.xferEta, cmp),

		                   (self.xferEta, icmp),
		                   (DCXfer.getSpeed, cmp),
		                   (self.getXferProgress, cmp),
		                   (self.getXferPath, icmp),
		                   (DCXfer.getType, cmp) ]
		self.sortAlgo = 3

		self.list = wxListCtrl(self, 1, style = wxLC_REPORT | wxLC_VRULES)
		self.menu = wxMenu()

		self.list.InsertColumn(0, "Type")
		self.list.InsertColumn(1, "File")
		self.list.InsertColumn(2, "Progress", wxLIST_FORMAT_RIGHT)
		self.list.InsertColumn(3, "Speed", wxLIST_FORMAT_RIGHT)
		self.list.InsertColumn(4, "ETA", wxLIST_FORMAT_RIGHT)
		self.list.SetColumnWidth(0, 20)

		vLayout = wxBoxSizer(wxVERTICAL)
		vLayout.Add(self.list, 1, wxEXPAND)

		self.SetSizer(vLayout)
		self.Layout()

		EVT_LIST_COL_CLICK(self, 1, self.setSortAlgo)
		EVT_LIST_ITEM_ACTIVATED(self.list, 1, self.closeXfer)
		self.Connect(1, 1, wxEVT_NULL, self.insertXfer)
		self.Connect(2, 2, wxEVT_NULL, self.removeXfer)
		self.Connect(3, 3, wxEVT_NULL, self.updateXfers)

		DCWorker.getWorker().getXferListener().registerListener(self)
		
	def setSortAlgo(self, event):
		col = event.GetColumn() + 1
		if self.sortAlgo == col:
			self.sortAlgo = -col
		else:
			self.sortAlgo = col

		access, comp = self.sortAlgos[self.sortAlgo]
		self.xfers = fullSort(self.xfers, access, comp)

		pos = 0
		for xfer in self.xfers:
			self.updateFields(pos, self.snap(xfer), 3)
			pos += 1

	def onNewXfer(self, xfer):
		self.lock.acquire()
		self.xfers.append(xfer)
		access, comp = self.sortAlgos[self.sortAlgo]
		oldPos, pos, self.xfers = partialSort(self.xfers, access, comp, xfer)
		self.lock.release()

		wxPostEvent(self, guiEvent(1, (pos, self.snap(xfer))))

	def onXferClosed(self, xfer):
		self.lock.acquire()
		pos = self.xfers.index(xfer)
		del self.xfers[pos]
		self.lock.release()

		wxPostEvent(self, guiEvent(2, pos))

	def insertXfer(self, event):
		pos = event.data[0]
		snap = event.data[1]

		self.list.Freeze()
		if snap[0] == DCXfer.TYPE_DOWNLOAD:
			self.list.InsertStringItem(pos, 'D')
		else:
			self.list.InsertStringItem(pos, 'U')
		self.updateFields(pos, snap, 2)
		self.list.Thaw()

	def removeXfer(self, event):
		self.list.DeleteItem(event.data)

	def updateXfers(self, event):
		self.list.Freeze()
		pos = 0
		for snap in event.data:
			self.updateFields(pos, snap, 3)
			pos += 1
		self.list.Thaw()

	def closeXfer(self, event):
		self.xfers[event.GetIndex()].stop()

	#=================#
	# Private section #
	#=================#

	def snap(self, xfer):
		item = xfer.getItem()
		if item == None: return None
		return (xfer.getType(), item.getPath(), xfer.getProgress(), xfer.getSpeed(), self.xferEta(xfer))

	def getXferPath(self, xfer):
		return xfer.getItem().getPath().lower()

	def getXferProgress(self, xfer):
		return xfer.getProgress()

	def update(self):
		self.lock.acquire()
		access, comp = self.sortAlgos[self.sortAlgo]
		self.xfers = fullSort(self.xfers, access, comp)
		snaps = filter(lambda i: i != None, map(self.snap, self.xfers))
		self.lock.release()

		wxPostEvent(self, guiEvent(3, snaps))

	def updateFields(self, pos, snap, mask):
		if mask & 1 == 1:
			if snap[0] == DCXfer.TYPE_DOWNLOAD:
				self.list.SetStringItem(pos, 0, 'D')
			else:
				self.list.SetStringItem(pos, 0, 'U')

		if mask & 2 == 2:
			self.list.SetStringItem(pos, 1, os.path.basename(snap[1]))
			self.list.SetStringItem(pos, 2, '%.1f%%' % snap[2])
			self.list.SetStringItem(pos, 3, formatSpeed(snap[3]))
			self.list.SetStringItem(pos, 4, self.formatEta(snap[4]))

	def xferEta(self, xfer):
		speed = xfer.getSpeed()
		if xfer.getSpeed() > 0:
			secs = xfer.getSizeRemaining() / speed
		else:
			secs = 0

		return secs

	def formatEta(self, secs):
		part = secs % 3600
		h = (secs - part) / 3600
		if h > 9999: return '00:00:00'

		secs = part

		part = secs % 60
		m = (secs - part) / 60
		secs = part

		return "%.2d:%.2d:%.2d" % (h, m, secs)
