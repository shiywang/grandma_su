from channels.generic.websocket import WebsocketConsumer


class SensorDataConsumer(WebsocketConsumer):
    data_topic = "userdata"
    
    def connect(self):
        print("acceptted")
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    def send(self, data_string):
        self.send(data_string="%s %s" % (self.data_topic, json.dumps(data)))


sensorDataConsumer = SensorDataConsumer()
