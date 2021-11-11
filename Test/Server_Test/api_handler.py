import os
import requests
import queue, threading, json

#api_user = "admin"
#api_password = "uched4123"

api_user = "test"
api_password = "test"
base_url = "http://127.0.0.1:8000/"
request_headers = {'Content-Type': 'application/json',}

class Api_Handler(threading.Thread):
	def __init__(self):
		super(Api_Handler, self).__init__()
		self.__output_queue = queue.Queue()
		self.__function_queue = queue.Queue()
		self.timeout = 1.0/60

	def onThread(self, function, *args, **kwargs):
		self.__function_queue.put((function, args, kwargs))

	def create_senior(self, data):
		r = requests.post(base_url+"seniors/", headers=request_headers, auth=(api_user, api_password), data=data)
		if r.status_code == 201:
			return True
		else:
			print(r.json())
			return False

	def delete_user(self, device_id):
		r = requests.delete(base_url+"seniors/"+device_id, auth=(api_user, api_password))

	def send_data(self, senior):
		device_type = senior.device.type.name
		data = senior.get_data()
		url = base_url + "sensordata/" + device_type + '/'
		r = requests.post(url, headers=request_headers, auth=(api_user, api_password), data=json.dumps(data))

	def send_ping(self, senior):
		data = {
			"device_id": senior.id,
			"battery": senior.get_battery(),
		}
		url = base_url + "ping/"
		r = requests.post(url, headers=request_headers, auth=(api_user, api_password), data=json.dumps(data))

	def run(self):
		print("Starting API Handler")
		while True:
			try:
				# Get functions called on this thread
				function, args, kwargs = self.__function_queue.get(timeout=self.timeout)
				function(*args, **kwargs)			
			except Exception as e:
				pass


# to be called from another thread on program exit
def custom_senior_delete(device_id):
	r = requests.delete(base_url+"seniors/"+device_id, auth=(api_user, api_password))


def custom_create_senior(data):
	r = requests.post(base_url+"seniors/", headers=request_headers, auth=(api_user, api_password), data=data)
	if r.status_code == 201:
		return True
	else:
		print(r.json())
		return False


api_handler = Api_Handler()
