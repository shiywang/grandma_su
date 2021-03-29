import serial
import threading
import time
from logger.logger import Logger, enum
from server_queue import serverQueue

start_byte = 0xAA

class UartReader(threading.Thread, Logger):
	def __init__(self, port):
		threading.Thread.__init__(self)
		Logger.__init__(self, "UART")
		self.__port_num__ = port
		self.__port__ = serial.Serial(port)
		
		self.read_buf = []
		self.read_pointer = 0
		self.state = None
		
	def run(self):
		self.debug("Starting Loop")
		states = enum("START_BYTE", "LENGTH", "DATA")
		self.state = states.START_BYTE					# Current state machine state
		read_len = 0									# Length of serial data to read
		
		while True:
			ch = self.__port__.read()
			
			if self.state == states.START_BYTE:
				if ch == start_byte:
					self.state = states.LENGTH
					continue
					
			elif self.state == states.LENGTH:
				read_len = int.from_bytes(ch, 'big')
				data = self.__port__.read(read_len)
				serverQueue.add([x for x in data])		# List Comprehension changes bytes to int
				
		
		
