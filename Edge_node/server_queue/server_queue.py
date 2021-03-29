import os, Queue
from logger.logger import Logger, enum

class ServerQueue(Logger):
	def __init__(self):
		Logger.__init__(self, "ServerQueue")
		self.__queue__ = Queue.Queue()
		
	def add(self, pkt):
		self.debug("Adding element")
		self.__queue__.put(pkt)
		
	def get(self):
		return self.__queue__.get()
		
serverQueue = ServerQueue()		# Single instance of serverQueue
		
