#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket as sckt
import select as slct
import re

import defaults


host =  '104.248.196.50'
if len(sys.argv) >= 2:
	host =  sys.argv[1]

sys.stdout.write('Choose your ID: ')
username = raw_input()

socket = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
sys.stdout.write('Connecting to: ' + host + '\n')
sys.stdout.flush()
socket.connect((host, defaults.PORT))
socket.send(defaults.protocol(username, 'server', '/set uid ' + username))

running = True
recepient = 'server'
while running:
	read, write, exceptions = slct.select([sys.stdin, socket], [], [], 0)
	for inpt in read:
		if inpt == socket:
			data = inpt.recv(1024)
			if data:
				result = re.match(defaults.PROTOCOL_RE, data)
				print(result.group(3).rjust(45))
			else:
				print('Connection closed by server, exiting')
				running = False
		else:
			msg = raw_input()
			if msg[:1] == '/':
				msg = msg[1:].split()
				if msg[0] == 'user':
					recepient = msg[1]
				elif msg[0] == 'exit':
					running = False
			else:
				socket.send(defaults.protocol(username, recepient, msg))

socket.close()
