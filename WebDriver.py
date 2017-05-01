import PixelWall
import PIL

import socket
import thread
import json
import os

#API_key = "CfyzWTBD1D2utgMaEgNkrI6RtSIEqPNlI7PnA5J1"

class WebInterface():
	def __init__(self,EngineReference,APIcall,ip = "192.168.0.2",port = 4300,key = "eXample0"):
		self.ip = ip
		self.port = port
		self.ER = EngineReference
		self.API = APIcall
		self.key = key

	def Run(self):
		addr = (self.ip,self.port)
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(addr)
		serversocket.listen(2)
		print "***|SERVER started on %s:%s with buffer size %s bytes|***" % ("192.168.0.2",4300,128)
		while 1:
			clientsocket, clientaddr = serversocket.accept()
			thread.start_new_thread(Connection, (clientsocket, clientaddr, self.API, self.key))
		serversocket.close()


class Connection():
	def __init__(self, clSocket, clAddr, clAPI, key):
		self.clSocket = clSocket
		self.clAddr = clAddr
		self.clAPI = clAPI
		self.clKey = key
		self.handler()

	def handler(self):
		print "[+][CON] Established " + str(self.clAddr)
		while 1:
			try:
				rec_data = self.clSocket.recv(1024)#Decode received Content
			except socket.error,e:
				print "[!][CRITICAL] socket error"
				break;
			if not rec_data:
				break
			self.API(rec_data)

	def API(self,rec_data):
		packet = Connection.decodePacket(rec_data)
		details = Connection.decodeParameters(packet["Path"])
		if not "key" in details:
			self.send(json.dumps({"response":{"status":"failed","message":"no device key given!","key":"invalid"}}),"application/json")
			return

		if not details["key"] == self.clKey:
			self.send(json.dumps({"response":{"status":"failed","message":"invalid device key!","key":"invalid"}}),"application/json")
			return

		if details["sub"] in self.clAPI.calls:
			print details["sub"]
			self.clAPI.calls[details["sub"]](details,self)
			return
		self.send(json.dumps({"response":{"status":"failed","message":"invalid api call","key":"valid"}}),"application/json")

	@staticmethod
	def decodeParameters(url):
			c = url
			if not "?" in c:return {};
			q = c.split("?")

			if "&" in c:
				d = q[1].split("&")
			else:
				d = {q[1]}
			p = dict()
			for a in d:
				if "=" in a:
					b = a.split("="); p[b[0]] = b[1]
			p["sub"] = q[0]
			return p

	@staticmethod
	def generatepacket(type, data):
		return 'HTTP/1.1 200 OK' + '\n' + 'Access-Control-Allow-Origin: *\nCache-Control: no-cache, no-store, must-revalidate' + '\n' + 'Pragma: no-cache' + '\n' + 'Expires: 0' + '\n' + 'Content-length: ' + str(len(data)) + '\n'+ type+ '\n' + '\n' + data

	def send(self, data, type):
		self.clSocket.send(Connection.generatepacket(type, data))

	@staticmethod
	def decodePacket(raw):
		raw_headers = raw.split("\r\n");headers = dict();
		if raw_headers[0][:3] == "OPT":
			headers["Request"] = "OPT"
		else:
			headers["Request"] = "GET"
		headers["Path"] = raw_headers[0].split(" ")[1]
		headers["Version"] = raw_headers[0].split(" ")[2]
		for head in raw_headers:
			if ":" in head:
				tmp = head.split(":")
				headers[tmp[0]] = tmp[1]
			elif len(head) > 1:
				headers["Content"] = head
		return headers
