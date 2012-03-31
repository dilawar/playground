# This file is part of pyDC software
# Copyright 2002-2003 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

from AsyncSocket import *
from EventGenerator import *
from Job import *
from DNS import DNSError
from DCChallenge import *
from DCFileList import *
from DCUser import *
from DCXfer import *
from socket import inet_aton, error
from threading import Lock
import time
import DCWorker

class DCHub(object, Job, EventGenerator):
	STATUS_CONNECTING = 1
	STATUS_CONNECTED = 2
	STATUS_CLOSED = 3

	LOG_STATUS = 1
	LOG_CHAT = 2
	LOG_PRIVCHAT = 3
	LOG_ERROR = 4

	USER_NORMAL = 1
	USER_FILESERVER = 4
	USER_SPEEDUSER = 8
	USER_AWAY_FLAG = 2

	MAX_LOG_ROWS = 2000
	RECONNECTION_DELAY = 30

	def __init__(self, addr):
		EventGenerator.__init__(self)

		self._addr = None
		self._status = 0
		self.logged = 0
		self.userNick = DCWorker.getWorker().user.nick
		self.userStatus = DCHub.USER_NORMAL
		self.delay = None
		self._users = {}
		self._log = []
		self.opLock = Lock()

		self._addr = self.parseAddress(addr)
		self.reset()

	def reset(self):
		if self._addr != None:
			self._name = self._addr[0]
		else:
			self._name = 'unknown'
		self.sock = None
		self._size = long(0)
		self.cmdQueue = []
		self.buf = ''

	def disconnect(self):
		self.stop()

	def startSearch(self, search, active):
		self.opLock.acquire()

		worker = DCWorker.getWorker()
		cmd = '$Search '
		if active:
			cmd += '%s:%d ' % (worker.getLocalAddress(), worker.getSettings().port)
		else:
			cmd += 'Hub:%s ' % self.userNick

		cmd += 'F?F?0?1?'
		for i in search.getPattern().split(' '):
			cmd += i + "$"

		self.cmdQueue.append(cmd[:-1] + '|')
		self.opLock.release()

	def requireConnection(self, nick):
		self.opLock.acquire()
		worker = DCWorker.getWorker()

		if worker.getSettings().active:
			self.cmdQueue.append('$ConnectToMe %s %s:%d|' % (nick, worker.getLocalAddress(), worker.getSettings().port))
		else:
			self.cmdQueue.append('$RevConnectToMe %s %s|' % (self.userNick, nick))

		self.opLock.release()

	def updateInfo(self):
		info = self.buildInfo()
		self.appendLogRow(self.LOG_STATUS, 'Updating user info...')

		self.opLock.acquire()
		self.cmdQueue.append('$MyINFO %s' % info)
		self.opLock.release()

	def setAway(self, away):
		if away:
			if self.userStatus & DCHub.USER_AWAY_FLAG:
				return
			else:
				txt = 'on'
				self.userStatus += DCHub.USER_AWAY_FLAG
		else:
			if self.userStatus & DCHub.USER_AWAY_FLAG:
				txt = 'off'
				self.userStatus -= DCHub.USER_AWAY_FLAG
			else:
				return

		info = self.buildInfo()
		self.appendLogRow(self.LOG_STATUS, 'Away flag: %s.' % txt)

		self.opLock.acquire()
		self.cmdQueue.append('$MyINFO %s' % info)
		self.opLock.release()

	def sendMsg(self, msg, nick=None):
		if self._status != 2:
			self.appendLogRow(self.LOG_ERROR, 'You must be connected to send messages.')
			return

		self.opLock.acquire()
		if nick == None:
			self.cmdQueue.append('<%s> %s|' % (self.userNick, msg.replace('|', '_')))
		else:
			self.cmdQueue.append('$To: %s From: %s $<%s> %s|' % (nick, self.userNick, self.userNick, msg.replace('|', '_')))
		self.opLock.release()

	def poll(self):
		try:
			if self._status == 0:
				if self.delay != None:
					curtime = time.time()

					self.delay[0] -= curtime - self.delay[1]
					if self.delay[0] <= 0:
						self.delay = None
					else:
						self.delay[1] = curtime
						return 0

				self.appendLogRow(self.LOG_STATUS, "Connecting to " + self._addr[0] + ":" + str(self._addr[1]) + "...")
				self.sock = AsyncSocket()
				self.sock.connect(self._addr)
				self.setStatus(1)

			elif self._status == 1:
				self.sock.poll()
				if self.sock.isConnected():
					self.appendLogRow(self.LOG_STATUS, "Connection established.")
					self.setStatus(2)

			elif self._status == 2:
				self.opLock.acquire()
				if self.logged:
					for cmd in self.cmdQueue:
						self.sock.send(cmd)
						
				self.cmdQueue = []
				self.opLock.release()

				finished = self.sock.poll()
				self.buf += self.sock.recv()
				if len(self.buf) > 0:
					cmds = self.buf.split('|')
					if self.buf[-1] != "|":
						self.buf = cmds[-1]
						cmds = cmds[:-1]
					else:
						self.buf = ""

					for i in cmds:
						if len(i) > 0:
							res = self.parseCmd(i)
							if res == 0:
								self.setStatus(6)
								return 0
							elif res == 1:
								self.setStatus(3)
								return 0

				if finished:
					self.appendLogRow(self.LOG_ERROR, "Connection closed.")
					self.checkReconnection()

			elif self._status == 3:
				self.sock.close()
				if self.sock.poll():
					self.removeAllUsers()

					self.opLock.acquire()
					self.reset()
					if self._status == 3: self._status = 0
					self.opLock.release()

					self.lock.acquire()
					for listener in self.listeners:
						listener.onHubInfo(self)
					self.lock.release()

			elif self._status == 4:
				self.sendCmd('Quit', self.userNick)
				self.sock.poll()
				self.setStatus(5)
				
			elif self._status == 5:
				if self.sock.getBytesToSend() > 0:
					self.sock.poll()
				else:
					self.setStatus(6)

			elif self._status == 6:
				if self.sock != None:
					self.sock.close()
					if not self.sock.poll():
						return 0

				self.opLock.acquire()
				self.reset()
				self._status = 7
				self.opLock.release()

				self.removeAllUsers()

				self.lock.acquire()
				for listener in self.listeners:
					listener.onHubDisconnection(self)
				self.lock.release()

				return 1

			else:
				return 1

		except DNSError:
			self.appendLogRow(self.LOG_ERROR, 'Connection closed because of DNS error.')
			self.setStatus(6)

		except error:
			self.appendLogRow(self.LOG_ERROR, 'Connection closed because of socket error.')
			self.checkReconnection()

		return 0

	def stop(self):
		self.opLock.acquire()

		log = None
		if self._status < 4:
			self._status = (6, 6, 4, 6)[self._status]

			log = (self.LOG_STATUS, 'Connection aborted by user.\n')
			self._log.append(log)

		self.opLock.release()

		if log:
			self.lock.acquire()
			for listener in self.listeners:
				listener.onLogUpdate(self, log)
			self.lock.release()

	def getAddress(self):
		return self._addr

	def getName(self):
		return self._name

	def getUserNum(self):
		return len(self._users)

	def getUsers(self):
		self.opLock.acquire()
		users = []
		for user in self._users:
			users.append(self._users[user])
		self.opLock.release()

		return users

	def getUserByNick(self, nick):
		self.opLock.acquire()
		try:
			user = self._users[nick]
		except KeyError:
			user = None
		self.opLock.release()

		return user

	def getSize(self):
		return self._size

	def getLogRows(self):
		return self._log

	def getStatus(self):
		return (self.STATUS_CONNECTING,
			  self.STATUS_CONNECTING,
			  self.STATUS_CONNECTED,
			  self.STATUS_CONNECTING,
			  self.STATUS_CLOSED,
			  self.STATUS_CLOSED,
			  self.STATUS_CLOSED,
			  self.STATUS_CLOSED)[self._status]

	def isAlive(self):
		return (1,1,1,1,0,0,0,0)[self._status]

	#=================#
	# Private members #
	#=================#

	def parseAddress(self, addr):
		if addr.__class__ == str:
			pos = addr.find(':') 
			if pos != -1:
				try:
					return (addr[:pos], int(addr[pos+1:]))
				except ValueError:
					self.appendLogRow(self.LOG_ERROR, "Invalid address: \"" + addr + "\".")
					self.setStatus(6)
					return None
			else:
				return (addr, 411)
		else:
			return addr
			
	def checkReconnection(self):
		if self._status == 2 and self.logged and self.getUserNum() > 0:
			self.delay = [self.RECONNECTION_DELAY, time.time()]
			self.setStatus(3)
			self.appendLogRow(self.LOG_STATUS, "Reconnecting in %d seconds..." % self.delay[0])
		else:
			self.setStatus(6)

	def setStatus(self, status):
		self.opLock.acquire()
		if status > self._status:
			self._status = status
		self.opLock.release()

	def buildInfo(self):
		user = DCWorker.getWorker().getUser()
		info = "$ALL " + self.userNick + " "
		if user.description != None:
			info += user.description

		info += "$ $"
		if user.connection == DCUser.CONN_56K:
			info += "56Kbps"
		elif user.connection == DCUser.CONN_SATELLITE:
			info += "Satellite"
		elif user.connection == DCUser.CONN_DSL:
			info += "DSL"
		elif user.connection == DCUser.CONN_CABLE:
			info += "Cable"
		elif user.connection == DCUser.CONN_T1:
			info += "LAN(T1)"
		elif user.connection == DCUser.CONN_T3:
			info += "LAN(T3)"
		info += chr(self.userStatus) + "$"

		if user.email != None:
			info += user.email
		info += "$"

		if user.share == -1:
			info += "0"
		else:
			info += str(user.share)
		info += "$"

		return info

	def appendLogRow(self, type, text):
		self.opLock.acquire()
		row = (type, text + '\n')
		self._log.append(row)
		if len(self._log) > DCHub.MAX_LOG_ROWS:
			del self._log[0]
		self.opLock.release()

		self.lock.acquire()
		for listener in self.listeners:
			listener.onLogUpdate(self, row)
		self.lock.release()

	def addUser(self, user, askinfo = 1):
		if len(user.nick) == 0 or user.nick == self.userNick: return
		if self._users.has_key(user.nick):
			if user.op: self._users[user.nick].op = 1
			return

		user.hub = self
		if askinfo and user.connection == DCUser.CONN_NONE:
			self.sendCmd("GetINFO", user.nick, self.userNick)

		self.opLock.acquire()
		self._users[user.nick] = user
		self.opLock.release()

		self.lock.acquire()
		for listener in self.listeners:
			listener.onNewUser(self, user)
		self.lock.release()

	def removeUser(self, nick):
		self.opLock.acquire()
		try:
			user = self._users[nick]
		except KeyError:
			self.opLock.release()
			return

		user.hub = None
		if user.share > 0:
			self._size -= user.share

		del self._users[nick]
		self.opLock.release()

		self.lock.acquire()
		for listener in self.listeners:
			listener.onUserDisconnection(self, user)
		self.lock.release()

	def removeAllUsers(self):
		self.opLock.acquire()
		users = self._users
		self._users = {}
		self._size = 0
		self.opLock.release()

		self.lock.acquire()
		for listener in self.listeners:
			for nick in users:
				listener.onUserDisconnection(self, users[nick])
		self.lock.release()

	def parseCmd(self, cmd):
		if cmd[0] == '<': #Chat message
			self.appendLogRow(self.LOG_CHAT, cmd)
			return 2
		elif cmd[0] != "$":
			self.appendLogRow(self.LOG_ERROR, "Unknown command: " + cmd)
			return 2
			
		cmd = cmd[1:]
		try:
			pos = cmd.index(' ')
			cmdname = cmd[:pos]
		except ValueError:
			if cmd == "HubIsFull":
				self.appendLogRow(self.LOG_ERROR, "Hub is full; disconnected.")
				return 0
			else:
				#Discard silently
				return 0

		if cmdname == "Hello":
			user = DCUser()
			user.nick = cmd[pos+1:]
			self.addUser(user)

		elif cmdname == "MyINFO":
			try:
				if cmd[pos+1:pos+6] != "$ALL ": return 2
				cmd = cmd[pos+6:]

				#Nick
				pos = cmd.index(" ")
				nick = cmd[:pos]
				cmd = cmd[pos+1:]

				if nick == self.userNick:
					self.logged = 1
					return 2

				try:
					user = self._users[nick]
				except KeyError:
					user = DCUser()
					user.nick = nick
					self.addUser(user, 0)

				#Description
				pos = cmd.index("$ $")
				if pos != 0:
					user.description = cmd[:pos]
				else:
					user.description = None
				cmd = cmd[pos+3:]

				#Split remaining fields
				fields = cmd.split("$")
				if len(fields) != 4:
					raise ValueError
				if len(fields[3]) > 0:
					raise ValueError

				#Connection
				fields[0] = fields[0][:-1]	#get rid of speed class byte
				if fields[0] == "56Kbps":
					user.connection = DCUser.CONN_56K
				elif fields[0] == "Satellite":
					user.connection = DCUser.CONN_SATELLITE
				elif fields[0] == "DSL":
					user.connection = DCUser.CONN_DSL
				elif fields[0] == "Cable":
					user.connection = DCUser.CONN_CABLE
				elif fields[0] == "LAN(T1)":
					user.connection = DCUser.CONN_T1
				elif fields[0] == "LAN(T3)":
					user.connection = DCUser.CONN_T3

				#Email
				if len(fields[1]) != 0:
					user.email = fields[1]
				else:
					user.email = None

				#Share
				user.share = long(fields[2])
				self._size += user.share

				#Notify listeners of changes
				self.lock.acquire()
				for listener in self.listeners:
					listener.onUserInfo(self, user)
				self.lock.release()

			except ValueError:
				pass

		elif cmdname == "Search":
			cmd = cmd[7:]

			try:
				p1, p2 = cmd.index(':'), cmd.index(' ')
				addr = cmd[:p1]
				if addr == "Hub":
					activeSearch = 0
					addr = cmd[p1+1:p2]
				else:
					activeSearch = 1
					addr = (addr, int(cmd[p1+1:p2]))

				params = cmd[p2+1:].split('?')
				if len(params) != 5:
					raise ValueError
					
				if params[0] == 'F':
					limit = DCFileList.LIMIT_NONE
					size = 0
				else:
					if params[1] == 'F':
						limit = DCFileList.LIMIT_ATLEAST
					else:
						limit = DCFileList.LIMIT_ATMOST

					size = long(params[2])

				worker = DCWorker.getWorker()
				slots = [worker.getSettings().slots - worker.getUsedSlots(), worker.getSettings().slots]
				hubAddr = self.sock.getpeername()
				
				#Safety check
				if hubAddr == None: return 0

				for i in worker.getLocalLists():
					for r in i.search(params[4].replace('$', ' '), limit, size):
						data =  '$SR %s %s\5%d %d/%d\5%s (%s:%d)' % (self.userNick, r.getPath(), r.size, slots[0], slots[1], self._name, hubAddr[0], hubAddr[1])
						if activeSearch:
							worker.getSearchWorker().sendResult(addr, data + '|')
						else:
							data += '\5%s|' % addr
							self.sock.send(data)

			except ValueError:
				pass
				
		elif cmdname == 'SR':
			DCWorker.getWorker().getSearchWorker().passiveResult(cmd[pos+1:])

		elif cmdname == "Quit":
			self.removeUser(cmd[pos+1:])

		elif cmdname == "To:":
			try:
				idx = cmd.index('$') - 1
				nick = cmd[cmd[:idx].rindex(' ')+1:idx]
				self.appendLogRow(self.LOG_PRIVCHAT, '<%s> %s' % (nick, cmd[idx+2:]))
			except ValueError: pass

		elif cmdname == "ConnectToMe":
			addr = cmd[cmd.rindex(' ')+1:].split(':')
			try: addr = (addr[0], int(addr[1]))
			except ValueError: pass

			sock = AsyncSocket()
			sock.connect(addr)
			DCWorker.getWorker().addJob(DCXfer(sock))
			
		elif cmdname == 'RevConnectToMe':
                	if not DCWorker.getWorker().getSettings().active: return 2
			self.requireConnection(cmd[cmd.index(' ')+1:cmd.rindex(' ')])
			
		elif cmdname == "LogedIn":
			user = DCUser()
			user.op = 1
			user.nick = cmd[pos+1:]
			self.addUser(user)

		elif cmdname == "NickList":
			nicks = cmd[pos+1:].split("$$")

			for nick in nicks:
				user = DCUser()
				user.nick = nick
				self.addUser(user)

		elif cmdname == "OpList":
			nicks = cmd[pos+1:].split("$$")

			for nick in nicks:
				user = DCUser()
				user.op = 1
				user.nick = nick
				self.addUser(user)

		elif cmdname == "ForceMove":
			newAddr = cmd[pos+1:]
			if len(newAddr) == 0: return 0

			addr = self.parseAddress(newAddr)
			if addr == None: return 0

			self.appendLogRow(self.LOG_STATUS, "Redirected to \"" + newAddr + "\".")
			self._addr = addr
			
			return 1

		elif cmdname == "Lock":
			key = solveChallenge(cmd[pos+1:])
			if len(key) == 0:
				self.appendLogRow(self.LOG_ERROR, "Error while generating authkey.")
				return 0

			self.sendCmd("Key", key)
			self.sendCmd("ValidateNick", self.userNick)
			self.sendCmd("Version", "1.3")

			self.sendCmd("MyINFO", self.buildInfo())
			self.sendCmd("GetNickList")

		elif cmdname == "HubName":
			self._name = cmd[pos+1:]

			self.lock.acquire()
			for i in self.listeners:
				i.onHubInfo(self)
			self.lock.release()

		elif cmdname == "GetPass":
			self.appendLogRow(self.LOG_ERROR, "Hub requires password. Function not yet implemented.")
			return 0

		elif cmdname == 'ValidateDenide':
			self.appendLogRow(self.LOG_ERROR, "Authentication error; disconnected.")
			return 0

		#else:
		#	self.appendLogRow(self.LOG_ERROR, "Unknown command: " + cmd)

		return 2

	def sendCmd(self, cmd, *args):
		cmdstr = "$" + cmd
		for i in args:
			cmdstr += " " + i
		cmdstr += "|"

		self.sock.send(cmdstr)

	address = property(getAddress, None, None, None)
	name = property(getName, None, None, None)
	userNum = property(getUserNum, None, None, None)
	users = property(getUsers, None, None, None)
	size = property(getSize, None, None, None)
	logRows = property(getLogRows, None, None, None)
	status = property(getStatus, None, None, None)

class AddressAlreadySetError(Exception): pass
