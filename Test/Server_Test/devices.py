import os
from random import randint
import binascii, enum, time

class Device_Types(enum.Enum):
	ECG  = 1
	RR   = 2
	TEMP = 3
	SPO2 = 4


class Device:
	def __init__(self, low_range, high_range):
		self.lower  = low_range
		self.higher = high_range
		self.id		= binascii.hexlify(bytearray(os.urandom(6))).decode('ascii').upper()
		self.type   = None

	def get_value(self):
		return randint(self.lower, self.higher)


class ECG_Device(Device):
	def __init__(self):
		Device.__init__(self, -10, 10)
		self.type = Device_Types.ECG


class RR_Device(Device):
	def __init__(self):
		Device.__init__(self, 950, 1100)
		self.type = Device_Types.RR


class Temperature_Device(Device):
	def __init__(self):
		Device.__init__(self, 31, 40)
		self.type = Device_Types.TEMP


class SPO2_Device(Device):
	def __init__(self):
		Device.__init__(self, 31, 40)
		self.type = Device_Types.SPO2