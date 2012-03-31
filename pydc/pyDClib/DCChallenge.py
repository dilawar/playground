# This file is part of pyDC software
# Copyright 2002 Anakim Border <aborder@users.sourceforge.net>
#
# pyDC is released under the terms of GPL licence.

def solveChallenge(challenge):
	try:
		pos = challenge.rindex(' ')
	except ValueError:
		return ""
	challenge = challenge[:pos]
	clen = len(challenge)
	k = ""

	#Convert string to integer array
	b = []
	for i in challenge:
		b.append(ord(i))

	#First byte
	u = b[0]
	l = b[clen-1]
	o = b[clen-2]
	u = u^l^o^5;
	v = (((u<<8)|u)>>4) & 255
	k += encodeChar(v)

	#Other bytes
	for i in range(1, clen):
		u = b[i]
		l = b[i-1]
		u = u^l
		v = (((u<<8)|u)>>4) & 255
		k += encodeChar(v)

	return k

def encodeChar(c):
	if c in (0, 5):
		return "/%%DCN%03u%%/" % c
	elif c == ord('$'):
		return "/%DCN036%/"
	elif c == 96:
		return "/%DCN096%/"
	else:
		return chr(c)
