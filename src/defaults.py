# -*- coding: utf-8 -*-

PORT = 7373

CFG_PREP = '/set '
CFG_PREP_LEN = len(CFG_PREP)

PROTOCOL_RE = '^SCC_0.1:([0-9]+);(?:([a-zA-Z0-9_\-!§$%&()#+*~]+);){2}>>(.+)$'
def protocol(sender, recepient, message):
	return 'SCC_0.1:' + str(len(message)) + ';' + str(sender) + ';' + str(recepient) + ';>>' + str(message)
