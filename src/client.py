#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket as sckt
import select as slct
from OpenSSL import SSL

import defaults

host = '127.0.0.1'


sys.stdout.write('Choose your ID: ')
username = raw_input()

socket = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
socket.connect((host, defaults.PORT))
socket.send(defaults.protocol(username, 'server', '/set uid ' + username))

running = True
recepient = 'server'
while running:
	read, write, exceptions = slct.select([sys.stdin, socket], [], [], 0)
	for inpt in read:
		if inpt == socket:
			data = inpt.recv(1024)
			print(data)
		else:
			msg = raw_input()
			if msg[:1] == '/':
				msg = msg[1:].split()
				if msg[0] == 'user':
					recepient = msg[1]
			else:
				socket.send(defaults.protocol(username, recepient, msg))

socket.close()
