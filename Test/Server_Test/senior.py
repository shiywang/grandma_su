import os 
from random import randrange, choice
from devices import Device, SPO2_Device, RR_Device, Temperature_Device
from api_handler import api_handler, custom_senior_delete, custom_create_senior
from logger import Logger
import names, time, json


class Senior:
	def __init__(self, device, userdata):
		self.__name 	= userdata.get("name", None)
		self.__age  	= userdata.get("age" , None)
		self.__room 	= userdata.get("room", None)
		self.__gender 	= userdata.get("gender", None)

		self.device 	= device 
		self.id 		= device.id

	def get_battery(self):
		return 60

	def get_data(self):
		return {
			"device_id": self.id,
			"time": int(time.time()),
			"value" : self.device.get_value()
		}

	def __str__(self):
		return f"{self.__name}: {self.__age}, {self.id}, {self.__gender}"



class Senior_Manager(Logger):
	def __init__(self):
		Logger.__init__(self, "SP")
		self.__senior_list = []

	def make_senior(self):
		gender  = choice(['male', 'female'])
		device  = choice([RR_Device, Temperature_Device, SPO2_Device])()			# Online RR_Device for now
		name    =  names.get_full_name(gender=gender)

		userdata = {
			"age": randrange(50, 100), 
			"room_no": randrange(1, 200), 
			"gender": gender, 
			"name": name,
			"device_id": device.id,
			"device_type": device.type.name,
			"user": {
				"username": (name + str(randrange(0, 100))).replace(" ", ""),
				"email": (f"{name}@gmail.com").replace(" ", ""),
				"password": "pass1234",
			},
		}

		res = custom_create_senior(json.dumps(userdata))
		if res is True:
			senior = Senior(device, userdata)
			self.info(senior)
			return senior
		else:
			self.error("Failed to create senior")
			return None

	def delete_senior(self, senior):
		custom_senior_delete(senior.id)


senior_manager = Senior_Manager()