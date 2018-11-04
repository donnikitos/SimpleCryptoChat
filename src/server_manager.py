# -*- coding: utf-8 -*-
import sys
import Queue
import re

import defaults


class cons:
	@staticmethod
	def print_info(par, par2):
		sys.stdout.write(u'\u001b[32;1m' + str(par) + u': \u001b[0m' + str(par2) + '\n')

class client:
	def __init__(self, socket, address):
		cons.print_info('New client', address)
		self.socket = socket
		self.address = address
		self.uid = ''
		self.queue = Queue.Queue()

	def receive(self):
		input = self.socket.recv(1024)

		if input:
			result = re.match(defaults.PROTOCOL_RE, input)
			if result == None:
				return

			if result.group(2) == 'server' and result.group(3)[:defaults.CFG_PREP_LEN] == defaults.CFG_PREP:
				command = result.group(3)[defaults.CFG_PREP_LEN:]
				if command.split()[0] == 'uid':
					self.uid = command.split()[1]
				cons.print_info('Config', command)

				return [result.group(2), input]
			else:
				return [result.group(2), input]
		else:
			return False

	def send(self, message):
		self.socket.send(message)

	def kill(self):
		self.socket.close()
		del self.queue
		cons.print_info('Connection closed', self.uid + '(' + str(self.address) + ')')


class management:
	def __init__(self):
		self.inputs = []
		self.outputs = []
		self.clients = {}

	def reg_client(self, clnt):
		socket, address = clnt.accept()
		self.inputs.append(socket)
		self.clients[socket] = client(socket, address)

	def receive(self, clnt):
		result = self.clients[clnt].receive()

		if result:
			if result[0] == 'server':
				print(result[1])
			else:
				for k, v in self.clients.iteritems():
					if v.uid == result[0]:
						self.clients[clnt].queue.put(result[1])
						if clnt not in self.outputs:
							self.outputs.append(clnt)

						v.queue.put(result[1])
						if k not in self.outputs:
							self.outputs.append(k)
		else:
			if clnt in self.outputs:
				self.outputs.remove(clnt)

			self.clients[clnt].kill()
			del self.clients[clnt]
			self.inputs.remove(clnt)
