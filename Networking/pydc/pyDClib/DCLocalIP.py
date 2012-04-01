# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

import socket
import sys

def getLocalIP():
	ip = None
	try:
		# This way, as suggested by bdash, we always
		# find the IP of the interface connected to
		# the Internet.

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('www.google.com', 80))
		ip = s.getsockname()[0]
		s.close()
	except socket.error:
		raise LocalIPError
	except socket.gaierror:
		raise LocalIPError

	return ip

class LocalIPError(Exception): pass
