# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from threading import Lock
from Util import *
from wxPython.wx import *

from DCHub import DCHub
from DCHubEventListener import *
import DCWorker

class HubsPanel(wxPanel, DCHubEventListener):
	INFO_TIMEOUT = 3

	def __init__(self, parent, id):
		wxPanel.__init__(self, parent, id)

		self.hubs = []
		self.lock = Lock()
		self.sortAlgo = 3
		self.sortAlgos = [ None,
		                   (self.getHubName, cmp),
		                   (DCHub.getAddress, cmp),
		                   (DCHub.getUserNum, icmp),
		                   (DCHub.getSize, icmp),

		                   (DCHub.getSize, cmp),
		                   (DCHub.getUserNum, cmp),
		                   (DCHub.getAddress, icmp),
		                   (self.getHubName, icmp) ]
		self.timestamp = 0

		self.list = wxListCtrl(self, 1, style = wxLC_REPORT | wxLC_SINGLE_SEL | wxLC_VRULES)

		self.list.InsertColumn(0, 'Name')
		self.list.InsertColumn(1, 'Address')
		self.list.InsertColumn(2, 'Users', wxLIST_FORMAT_RIGHT)
		self.list.InsertColumn(3, 'Share', wxLIST_FORMAT_RIGHT)
		
		vLayout = wxBoxSizer(wxVERTICAL)
		vLayout.Add(self.list, 1, wxEXPAND | wxTOP, 5)
		
		self.SetSizer(vLayout)
		self.Layout()
		
		EVT_LIST_COL_CLICK(self, 1, self.setSortAlgo)
		EVT_LIST_ITEM_SELECTED(self.list, 1, self.onHubActivation)
		self.Connect(1, 1, wxEVT_NULL, self.addHub)
		self.Connect(2, 2, wxEVT_NULL, self.removeHub)
		self.Connect(3, 3, wxEVT_NULL, self.updateHubs)
		self.Connect(4, 4, wxEVT_NULL, self.chatMsg)

	def setSortAlgo(self, event):
		col = event.GetColumn() + 1
		if self.sortAlgo == col:
			self.sortAlgo = -col
		else:
			self.sortAlgo = col

		self.update()

	def onHubActivation(self, event):
		try: getMainWnd().setActiveJob(self.hubs[event.GetIndex()])
		except IndexError: pass

	def onNewHub(self, hub):
		self.lock.acquire()
		hub.registerListener(self)
		self.hubs.append(hub)
		access, comp = self.sortAlgos[self.sortAlgo]
		oldPos, pos, self.hubs = partialSort(self.hubs, access, comp, hub)
		self.lock.release()

		wxPostEvent(self, guiEvent(1, (pos, self.snap(hub))))

	def onHubDisconnection(self, hub):
		self.lock.acquire()
		pos = self.hubs.index(hub)
		del self.hubs[pos]
		self.lock.release()

		wxPostEvent(self, guiEvent(2, pos))

	def onLogUpdate(self, hub, row):
		if row[0] == DCHub.LOG_PRIVCHAT:
			wxPostEvent(self, guiEvent(4, (hub, row[1])))

	def addHub(self, event):
		pos = event.data[0]
		snap = event.data[1]

		self.list.Freeze()
		self.list.InsertStringItem(pos, snap[0])
		self.updateFields(pos, snap, 2)
		self.list.Thaw()

	def removeHub(self, event):
		self.list.DeleteItem(event.data)

	def updateHubs(self, event):
		self.list.Freeze()
		pos = 0
		for snap in event.data:
			self.updateFields(pos, snap, 3)
			pos += 1
		self.list.Thaw()

	def chatMsg(self, event):
		hub = event.data[0]
		row = event.data[1]

		idx = row.index('>')
		nick = row[1:idx]
		msg = row[idx+2:]

		chat = getMainWnd().getChat(nick, hub)
		if chat: chat.appendMsg(msg)

	#=================#
	# Private section #
	#=================#

	def snap(self, hub):
		return (hub.getName(), hub.getAddress(), hub.getUserNum(), hub.getSize())

	def getHubName(self, hub):
		return hub.getHubName().lower()

	def update(self):
		self.lock.acquire()
		access, comp = self.sortAlgos[self.sortAlgo]
		self.hubs = fullSort(self.hubs, access, comp)
		snaps = map(self.snap, self.hubs)
		self.lock.release()

		wxPostEvent(self, guiEvent(3, snaps))

	def updateFields(self, pos, snap, mask):
		if mask & 1:
			self.list.SetStringItem(pos, 0, snap[0])
		if mask & 2:
			self.list.SetStringItem(pos, 1, '%s:%d' % snap[1])
			self.list.SetStringItem(pos, 2, str(snap[2]))
			self.list.SetStringItem(pos, 3, formatSize(snap[3]))
