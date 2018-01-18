#from neolib import neoutil,neo_class
#import sys
import time
#import neolib
#import http
#import  json
import socket
#import http.client
import logging
import threading
from logging import handlers
import socketserver
# create a socket object

class NeoBASEServer():
	def __init__(self, port, RequestHandlerClass, etc_param=None):
		self.debug = self.def_debug

		self.init()
		self.debug("%s __init__", self.__class__.__name__)
		self.debug("WAITING %d", port)
		self.RequestHandlerClass =RequestHandlerClass
		self.etc_param = etc_param

	def def_debug(self, fmt, *args):
		print(fmt % (*args,))
		pass

	def init(self):
		None

class NeoTCPServer(NeoBASEServer,socketserver.TCPServer):
	def __init__(self, port, RequestHandlerClass, etc_param=None):

		NeoBASEServer.__init__(self, port, RequestHandlerClass,etc_param)
		socketserver.TCPServer.__init__(self, ('0.0.0.0',port), RequestHandlerClass)
		None

class NeoUDPServer(NeoBASEServer,socketserver.UDPServer):
	def __init__(self, port, RequestHandlerClass, etc_param=None):

		NeoBASEServer.__init__(self, port, RequestHandlerClass,etc_param)
		socketserver.UDPServer.__init__(self, ('0.0.0.0',port), RequestHandlerClass)
		None


class baseHandleClient:
	def __init__(self, clientsocket):
		self.clientsocket = clientsocket
		self.init()

	def	init(self):
		None
	def run(self):
		None

	def bf_run(self,server_handle):
		None

	def af_run(self,server_handle):
		None


class BaseHandleServer:
	def __init__(self, port, obj_client_handler):
		self.obj_client_handler = obj_client_handler
		self.port = port
		self.debug = self.def_debug
		self.init()
		self.debug("%s __init__", self.__class__.__name__)

	def def_debug(self, fmt, *args):
		print(fmt % (*args,))

	def init(self):
		None

	def worker(self,clientsocket, addr,idx):
		handleClient = self.obj_client_handler(clientsocket)
		handleClient.bf_run(self)
		handleClient.run();
		handleClient.af_run(self)
		del (self.threads[idx])
		self.clientsocket.close()
		#self.threads.remove(t)
		None


	def run(self):
		idx = 0
		self.threads = {}
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# get local machine name
		host = '0.0.0.0'

		# bind to the port
		serversocket.bind((host, self.port))
		# queue up to 5 requests
		serversocket.listen(50)

		while True:
			# establish a connection
			self.debug('waiting')
			self.clientsocket, addr = serversocket.accept()
			#handle = HandleClient()
			self.debug("Got a connection from %s , thread num:%d" % (str(addr),len(self.threads)+1))
			t = threading.Thread(target=self.worker,args= (self.clientsocket, addr,idx))
			self.debug(t)
			self.threads[idx]= t
			t.start()
			idx += 1

class SampleEchoHandleClient(baseHandleClient):
	def	init(self):
		None
	def run(self):
		try:
			buff = self.clientsocket.recv(128)
			print(buff)
			if buff == b'':
				return

			time.sleep(0.1)
			self.clientsocket.send(buff)
			time.sleep(0.1)
		except Exception as ext:
			print(ext)
			return


class HandleServerWithLogging(BaseHandleServer):
	def init(self):
		self.handler = handlers.TimedRotatingFileHandler(filename="log.txt", when='D')
		self.logger = self.createLogger("tcp_giant_auth", self.handler)

		self.debug = self.logger.debug

	def createLogger(self, loggename, handler):

		self.loggename = loggename
		# create logger
		self.logger = logging.getLogger(loggename)
		self.logger.setLevel(logging.DEBUG)

		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)

		# create formatter
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		# add formatter to ch
		ch.setFormatter(formatter)
		handler.setFormatter(formatter)
		# add ch to logger
		self.logger.addHandler(ch)
		self.logger.addHandler(handler)
		return self.logger


#HandleClient().Test()
#HandleClient().RunServer()
if __name__ == '__main__':
	HandleServerWithLogging(5510,SampleEchoHandleClient).run()

