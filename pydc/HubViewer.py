# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from EventGenerator import *
from JobViewer import *
from JobViewerInfo import *
from Util import *
from wxPython.wx import *
import time

from DCHub import *
from DCHubEventListener import *
from DCUser import *
import DCWorker

class HubViewer(wxPanel, EventGenerator, JobViewer, DCHubEventListener):
	def __init__(self, parent, id, info):
		wxPanel.__init__(self, parent, id)
		EventGenerator.__init__(self)
		JobViewer.__init__(self, info)

		self.sortAlgos = [ None,
		                   (DCUser.isOp, icmp),
		                   (self.getNick, cmp),
		                   (DCUser.getDescription, cmp),
		                   (DCUser.getEmail, cmp),
		                   (DCUser.getConnection, icmp),
		                   (DCUser.getShare, icmp),

		                   (DCUser.getShare, cmp),
		                   (DCUser.getConnection, cmp),
		                   (DCUser.getEmail, icmp),
		                   (DCUser.getDescription, icmp),
		                   (self.getNick, icmp),
		                   (DCUser.isOp, cmp) ]
		self.users = []
		self.allowUpdates = 0
		self.updateTime = 0
		self.updates = []
		self.menuId = -1

		self.notebook = wxNotebook(self, -1)

		chatPanel = wxPanel(self.notebook, -1)
		self.text = wxTextCtrl(chatPanel, -1, style = wxTE_MULTILINE | wxTE_RICH)
		self.msg = wxTextCtrl(chatPanel, 1, style = wxTE_PROCESS_ENTER)

		chLayout = wxBoxSizer(wxHORIZONTAL)
		chLayout.Add(self.msg, 1, wxEXPAND)

		cvLayout = wxBoxSizer(wxVERTICAL)
		cvLayout.Add(self.text, 1, wxEXPAND)
		cvLayout.Add(chLayout, 0, wxEXPAND | wxBOTTOM | wxTOP, 5)
		chatPanel.SetSizer(cvLayout)

		self.notebook.AddPage(chatPanel, 'Chat')

		usersPanel = wxPanel(self.notebook, -1)
		self.list = wxListCtrl(usersPanel, 2, style = wxLC_REPORT | wxLC_VRULES | wxLC_SINGLE_SEL)
		self.list.InsertColumn(0, 'OP')
		self.list.InsertColumn(1, 'Nick')
		self.list.InsertColumn(2, 'Description')
		self.list.InsertColumn(3, 'Email')
		self.list.InsertColumn(4, 'Connection')
		self.list.InsertColumn(5, 'Share', wxLIST_FORMAT_RIGHT)
		self.list.SetColumnWidth(0, 20)
		self.list.SetColumnWidth(4, 20)

		uvLayout = wxBoxSizer(wxVERTICAL)
		uvLayout.Add(self.list, 1, wxEXPAND)
		usersPanel.SetSizer(uvLayout)

		self.notebook.AddPage(usersPanel, 'Users')

		dismiss = wxButton(self, 3, 'Dismiss')
		disconnect = wxButton(self, 4, 'Disconnect')
		
		bhLayout = wxBoxSizer(wxHORIZONTAL)
		bhLayout.Add(dismiss, 0, wxRIGHT, 10)
		bhLayout.Add(disconnect)
		
		vLayout = wxBoxSizer(wxVERTICAL)
		vLayout.Add(self.notebook, 1, wxEXPAND)
		vLayout.Add(bhLayout, 0, wxALIGN_CENTER | wxBOTTOM | wxTOP, 5)

		self.SetSizer(vLayout)
		self.Layout()

		EVT_TEXT_ENTER(self, 1, self.onMsg)
		EVT_LIST_COL_CLICK(self, 2, self.setSortAlgo)
		EVT_LIST_ITEM_RIGHT_CLICK(self, 2, self.onUserOptions)
		EVT_LIST_ITEM_ACTIVATED(self, 2, self.onUserSelected)
		EVT_MENU(self.list, 10000, self.onPopupSelection)
		EVT_BUTTON(self, 3, self.onDismiss)
		EVT_BUTTON(self, 4, self.onDisconnect)
		self.Connect(1, 1, wxEVT_NULL, self.updateInfo)
		self.Connect(2, 2, wxEVT_NULL, self.addUser)
		self.Connect(3, 3, wxEVT_NULL, self.removeUser)
		self.Connect(4, 4, wxEVT_NULL, self.updateUser)
		self.Connect(5, 5, wxEVT_NULL, self.addLogRow)
		
		self.notebook.SetSelection(self.info.page)

		self.text.SetEditable(0)
		rows = self.info.getJob().getLogRows()
		if len(rows):
			self.text.Freeze()
			for i in rows: self.appendText(i)
			self.text.Thaw()
			if wxPlatform == '__WXMSW__':
				self.text.ScrollPages(9999)
			else:
				lastPos = max(self.text.GetLastPosition() - 1, 0)
				self.text.ShowPosition(lastPos)

		if self.info.msgText != None:
			self.msg.SetValue(self.info.msgText)

		self.sortAlgo = self.info.sortAlgo
		for col in range(len(self.info.columnWidth)):
			self.list.SetColumnWidth(col, self.info.columnWidth[col])

		self.users.append(DCWorker.getWorker().getSettings().user)
		for user in self.info.getJob().getUsers():
			self.users.append(user)
		
		if len(self.users) > 1:
			self.allowUpdates = 1

			access, comp = self.sortAlgos[self.sortAlgo]
			self.users = fullSort(self.users, access, comp)
			self.buildList()

	def Destroy(self):
		self.info.page = self.notebook.GetSelection()
		if self.info.page == -1: self.info.page = 0

		self.info.msgText = self.msg.GetValue()
		self.info.sortAlgo = self.sortAlgo

		self.info.columnWidth = []
		for col in range(self.list.GetColumnCount()):
			self.info.columnWidth.append(self.list.GetColumnWidth(col))

		JobViewer.__del__(self)
		return wxPanel.Destroy(self)

	def getTitle(self):
		return self.info.getJob().getName()

	def onMsg(self, event):
		text = self.msg.GetValue()
		if len(text) == 0: return

		if text[0] == '/':
			if text[1:] == 'away':
				hub = self.info.getJob()
				hub.setAway(not (hub.userStatus & DCHub.USER_AWAY_FLAG))
			elif text[1:] == 'info':
				self.info.getJob().updateInfo()
			elif text[1:] == 'refresh':
				DCWorker.getWorker().refreshLocalList()
			else:
				self.addLogRow((DCHub.LOG_ERROR, 'Unknown command \'%s\'.' % text[1:]))

		elif text[0] == '<':
			try:
				pos = text.find('>')
				if pos == -1:
					dialog = wxMessageDialog(self, "Invalid private chat text.", "Error", wxICON_ERROR)
					dialog.ShowModal()
					raise 0

				nick = text[1:pos]
				if self.info.getJob().getUserByNick(nick) == None:
					dialog = wxMessageDialog(self, "No user with that nick.", "Error", wxICON_ERROR)
					dialog.ShowModal()
					raise 0

				text = text[pos+1:]
			except:
				text = None

			self.msg.SetValue('')
			if text: getMainWnd().getChat(nick, self.info.getJob()).sendMsg(text)
			return

		else:
			self.info.getJob().sendMsg(text)

		self.msg.SetValue('')

	def onUserSelected(self, event):
		nick = self.users[event.GetIndex()].getNick()
		getMainWnd().getChat(nick, self.info.getJob())

	def onUserOptions(self, event):
		pnt = event.GetPoint()
		nick = self.users[event.GetIndex()].getNick()
		self.list.SetItemState(event.GetIndex(), wxLIST_STATE_SELECTED, wxLIST_STATE_SELECTED)

		menu = wxMenu()
		menu.Append(10000, 'Chat')
		self.list.PopupMenu(menu, pnt)

		if self.menuId == 10000:
			getMainWnd().getChat(nick, self.info.getJob())

		self.menuId = -1

	def onPopupSelection(self, event):
		self.menuId = event.GetId()

	def onDismiss(self, event):
		self.lock.acquire()
		for listener in self.listeners:
			listener.onViewerClosed(self ,0)
		self.lock.release()
		
		self.Destroy()

	def onDisconnect(self, event):
		self.lock.acquire()
		self.info.getJob().stop()
		for listener in self.listeners:
			listener.onViewerClosed(self, 1)
		self.lock.release()
		
		wxYield()    #prevents segfault
		self.Destroy()
		
	def setSortAlgo(self, event):
		col = event.GetColumn() + 1
		if self.sortAlgo == col:
			self.sortAlgo = -col
		else:
			self.sortAlgo = col

		access, comp = self.sortAlgos[self.sortAlgo]
		self.users = fullSort(self.users, access, comp)

		pos = 0
		for user in self.users:
			self.list.SetStringItem(pos, 0, str(user.op))
			self.list.SetStringItem(pos, 1, user.nick)
			self.update(user, pos)
			pos += 1

	def onHubInfo(self, hub):
		if self.processEvents:
			wxPostEvent(self, wxPyEvent(1))

	def onNewUser(self, hub, user):
		if self.processEvents:
			wxPostEvent(self, guiEvent(2, user))

	def onUserDisconnection(self, hub, user):
		if self.processEvents:
			wxPostEvent(self, guiEvent(3, user))

	def onUserInfo(self, hub, user):
		if self.processEvents:
			wxPostEvent(self, guiEvent(4, user))

	def onLogUpdate(self, hub, row):
		if self.processEvents:
			wxPostEvent(self, guiEvent(5, row))

	def buildList(self):
		pos = 0
		for user in self.users:
			self.list.InsertStringItem(pos, str(user.op))
			self.list.SetStringItem(pos, 1, user.nick)
			self.update(user, pos)
			pos += 1
			
	def updateInfo(self, event):
		title = self.getTitle()
		self.lock.acquire()
		for listener in self.listeners:
			listener.onViewerTitle(self, title)
        	self.lock.release()
		
	def addUser(self, event):
		user = event.data
		self.users.append(user)
		if not self.allowUpdates: return
		
		access, comp = self.sortAlgos[self.sortAlgo]
		oldPos, pos, self.users = partialSort(self.users, access, comp, user)

		self.list.InsertStringItem(pos, str(user.op))
		self.list.SetStringItem(pos, 1, user.nick)
		self.update(user, pos)

	def removeUser(self, event):
		pos = self.users.index(event.data)

		try:
			del self.users[pos]
			self.updates.remove(event.data)
		except ValueError: pass

		if not self.allowUpdates: return
		
		self.list.DeleteItem(pos)
		
	def updateUser(self, event):
		if not self.allowUpdates:
			self.allowUpdates = 1

			access, comp = self.sortAlgos[self.sortAlgo]
			self.users = fullSort(self.users, access, comp)
			self.buildList()
			return

		user = event.data
		self.updates.append(user)

		curtime = time.time()
		if curtime - self.updateTime < 0.5: return

		updates = self.updates[:40]
		self.updates = self.updates[40:]
		self.updateTime = curtime

		oldPos = []
		for user in updates:
			try: oldPos.append(self.users.index(user))
			except ValueError: oldPos.append(-1)

		access, comp = self.sortAlgos[self.sortAlgo]
		self.users = fullSort(self.users, access, comp)

		try:
			while 1:
				curUser = updates.pop()
				bpos = oldPos.pop()
				if bpos == -1: continue
				apos = self.users.index(curUser)

				if apos == bpos:
					self.update(curUser, apos)
				else:
					self.list.DeleteItem(bpos)

					self.list.InsertStringItem(apos, str(curUser.op))
					self.list.SetStringItem(apos, 1, curUser.nick)
					self.update(curUser, apos)
		except IndexError: pass

	def addLogRow(self, event):
		self.text.Freeze()
		if self.text.GetNumberOfLines() == DCHub.MAX_LOG_ROWS:
			self.text.Remove(0, self.text.GetLineLength(0))
		self.appendText(event.data)
		self.text.Thaw()

		lastPos = max(self.text.GetLastPosition() - 1, 0)
		self.text.ShowPosition(lastPos);

	#=================#
	# Private section #
	#=================#

	def getNick(self, user):
		return user.getNick().lower()

	def appendText(self, row):
		msg = row[1].replace('\r', '')

		if row[0] == DCHub.LOG_STATUS:
			self.text.SetDefaultStyle(wxTextAttr(wxColor(0,128,128)))
			self.text.AppendText(msg)
			self.text.SetDefaultStyle(wxTextAttr('BLACK'))

		elif row[0] == DCHub.LOG_CHAT:
			self.text.AppendText(msg)

		#elif row[0] == DCHub.LOG_PRIVCHAT:
		#	self.text.AppendText('Priv: ' + msg)

		elif row[0] == DCHub.LOG_ERROR:
			self.text.SetDefaultStyle(wxTextAttr('RED'))
			self.text.AppendText(msg)
			self.text.SetDefaultStyle(wxTextAttr('BLACK'))

	def update(self, user, pos):
		if user.description == None:
			self.list.SetStringItem(pos, 2, '')
		else:
			self.list.SetStringItem(pos, 2, user.description)

		if user.email == None:
			self.list.SetStringItem(pos, 3, '')
		else:
			self.list.SetStringItem(pos, 3, user.email)

		self.list.SetStringItem(pos, 4, str(user.connection))

		if user.share == -1:
			self.list.SetStringItem(pos, 5, '')
		else:
			self.list.SetStringItem(pos, 5, formatSize(user.share))

class HubViewerInfo(JobViewerInfo):
	def __init__(self, hub):
		JobViewerInfo.__init__(self, hub)
		
		self.page = 0
		self.msgText = None
		self.sortAlgo = 2
		self.columnWidth = []

