#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket as sckt
import select as slct
import Queue

import defaults
import server_manager


socket = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
socket.setsockopt(sckt.SOL_SOCKET, sckt.SO_REUSEADDR, 1)
# socket.bind((sckt.gethostname(), defaults.PORT))
socket.bind(('', defaults.PORT))
socket.listen(5)

running = True
manager = server_manager.management()
while running:
	read, write, exceptions = slct.select([socket] + manager.inputs, manager.outputs, [], 0)

	for client in read:
		if client == socket:
			manager.reg_client(client)
		else:
			manager.receive(client)

	for client in write:
		try:
			msg = manager.clients[client].queue.get_nowait()
		except Queue.Empty:
			manager.outputs.remove(client)
		else:
			manager.clients[client].send(msg)

	for exc in exceptions:
		print(exc)

socket.close()
