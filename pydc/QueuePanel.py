# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import os.path
from wxPython.wx import *
from Util import *
from ViewerListener import *

from DCDownload import DCDownload
from DCQueueItem import *
from DCQueueEventListener import *
from DCXferListenerEventListener import *
import DCWorker

class QueuePanel(wxPanel, DCQueueEventListener, DCXferListenerEventListener, ViewerListener):
	def __init__(self, parent, id):
		wxPanel.__init__(self, parent, id)

		self.sortAlgo = 3
		self.sortAlgos = [ None,
		                   (DCQueueItem.getPath, cmp),
		                   (DCQueueItem.getStatus, icmp),
		                   (DCQueueItem.getProgress, icmp),
		                   (DCQueueItem.getSize, icmp),

		                   (DCQueueItem.getSize, cmp),
		                   (DCQueueItem.getProgress, cmp),
		                   (DCQueueItem.getStatus, cmp),
		                   (DCQueueItem.getPath, icmp) ]
		self.items = []

		self.list = wxListCtrl(self, 1, style = wxLC_REPORT | wxLC_SINGLE_SEL | wxLC_VRULES)

		self.list.InsertColumn(0, "File")
		self.list.InsertColumn(1, "Status")
		self.list.InsertColumn(2, "Progress", wxLIST_FORMAT_RIGHT)
		self.list.InsertColumn(3, "Size", wxLIST_FORMAT_RIGHT)

		vLayout = wxBoxSizer(wxVERTICAL)
		vLayout.Add(self.list, 1, wxEXPAND)

		self.SetSizer(vLayout)
		self.Layout()

		EVT_LIST_COL_CLICK(self, 1, self.setSortAlgo)
		EVT_LIST_ITEM_ACTIVATED(self, 1, self.onClose)
		self.Connect(1, 1, wxEVT_NULL, self.insertItem)
		self.Connect(2, 2, wxEVT_NULL, self.updateItem)
		self.Connect(3, 3, wxEVT_NULL, self.removeItem)

		queue = DCWorker.getWorker().getQueue()
		for item in queue.getItems():
			self.onNewItem(queue, item)
		
		queue.registerListener(self)
		DCWorker.getWorker().getXferListener().registerListener(self)

	def setSortAlgo(self, event):
		col = event.GetColumn() + 1
		if self.sortAlgo == col:
			self.sortAlgo = -col
		else:
			self.sortAlgo = col

		access, comp = self.sortAlgos[self.sortAlgo]
		self.items = fullSort(self.items, access, comp)

		pos = 0
		for item in self.items:
			self.list.SetStringItem(pos, 0, os.path.basename(item.path))
			self.update(pos, self.snap(item))
			pos += 1

	def onNewItem(self, queue, item):
		self.items.append(item)
		access, comp = self.sortAlgos[self.sortAlgo]
		oldPos, pos, self.items = partialSort(self.items, access, comp, item)

		wxPostEvent(self, guiEvent(1, (pos, self.snap(item))))

	def onItemStatus(self, queue, item):
		access, comp = self.sortAlgos[self.sortAlgo]
		oldPos, pos, self.items = partialSort(self.items, access, comp, item)

		wxPostEvent(self, guiEvent(2, (oldPos, pos, self.snap(item))))

	def onXferUpdate(self, xfer):
		if isinstance(xfer, DCDownload):
			self.onItemStatus(None, xfer.getItem())

	def onItemRemoved(self, queue, item):
		pos = self.items.index(item)
		del self.items[pos]

		wxPostEvent(self, guiEvent(3, pos))

	def onClose(self, event):
		queue = DCWorker.getWorker().getQueue()
		queue.removeItem(self.items[event.GetIndex()])

	#===================#
	#  Private members  #
	#===================#

	def snap(self, item):
		return (item.getPath(), item.getStatus(), item.getProgress(), item.getSize())

	def insertItem(self, event):
		pos = event.data[0]
		snap = event.data[1]

		self.list.InsertStringItem(pos, os.path.basename(snap[0]))
		self.update(pos, snap)

	def updateItem(self, event):
		oldPos = event.data[0]
		pos = event.data[1]
		snap = event.data[2]

		if oldPos != pos:
			self.list.DeleteItem(oldPos)
			self.list.InsertStringItem(pos, os.path.basename(snap[0]))

		self.update(pos, snap)

	def removeItem(self, event):
		self.list.DeleteItem(event.data)

	def update(self, pos, snap):
		if snap[1] == DCQueueItem.STATUS_WAITING:
			self.list.SetStringItem(pos, 1, "Waiting")
		elif snap[1] == DCQueueItem.STATUS_RUNNING:
			self.list.SetStringItem(pos, 1, "Running")
		elif snap[1] == DCQueueItem.STATUS_COMPLETED:
			self.list.SetStringItem(pos, 1, "Completed")
		elif snap[1] == DCQueueItem.STATUS_ERROR:
			self.list.SetStringItem(pos, 1, "Error")

		self.list.SetStringItem(pos, 2, "%.1f%%" % snap[2])
		self.list.SetStringItem(pos, 3, formatSize(snap[3]))
