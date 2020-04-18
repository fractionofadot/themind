#!/usr/bin/python3

import re
import os
import sys
import json

class CGIO():
	def __init__(self):
		self.method = os.environ['REQUEST_METHOD']

		self.methods = {
			'POST' : self._sanitizeInput( sys.stdin.read() ), 
			'GET' : self._sanitizeInput( os.environ['QUERY_STRING'] ) 
		}


	def _sanitizeInput(self, raw):
		allowed = re.compile("^[\w&=+]*$")
		if ( allowed.match(raw) ):
			return raw
		return None

	def _parseQuery(self, data):
	        output = {}

	        if not data:
	        	return {'error': "no data"} 

	        params = data.split("&")
	        for param in params:
	            key, value = param.split("=")
	            output[key] = value
	        return output

	def params(self):
		if self.method not in self.methods:
			return None

		return self._parseQuery( self.methods[self.method] )

	def header(self, ctype="html"):
		ctypes = {"html" : "Content-type: text/html", "json" : "Content-type: application/json"}
		if ctype in ctypes:
			print(ctypes[ctype])
			print("")
		else:
			print(ctype["html"])


