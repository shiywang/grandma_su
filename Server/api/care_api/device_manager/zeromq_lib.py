import os, json
import zmq 
from threading import Thread, RLock

ZEROMQ_SERVER = "0.0.0.0"
ZEROMQ_PORT   = "5456"

class ZeroMQ_Manager:
	def __init__(self):
		context = zmq.Context()
		self.socket = context.socket(zmq.PUB)
		self.socket.bind(f"tcp://{ZEROMQ_SERVER}:{ZEROMQ_PORT}")

		self.data_topic = "userdata"
		print(f"tcp://{ZEROMQ_SERVER}:{ZEROMQ_PORT}")

	def send(self, data):
		try:
			self.socket.send_string("%s %s" % (self.data_topic, json.dumps(data)))
		except Exception as e:
			pass 


zeroMQManager = ZeroMQ_Manager()