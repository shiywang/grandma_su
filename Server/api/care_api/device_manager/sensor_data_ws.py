from channels.generic.websocket import WebsocketConsumer
# from device_manager.data_medium import dataMedium
from device_manager.manager import onlineSeniorsDict
from data_api.models import Senior
from asgiref.sync import async_to_sync
import json

DEVICE_TIMEOUT = 60 * 5
MAX_DATA_ARRAY_LEN = 10


class SensorDataConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = 'event'
        self.room_group_name = self.room_name+"_sharif"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(self.room_group_name)
        self.accept()
        print("#######CONNECTED############")


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("DISCONNECED CODE: ",code)

    def receive(self, text_data=None):
        global onlineSeniorsDict

        print(" MESSAGE RECEIVED")
        print(text_data)
        data = json.loads(text_data)
        device_id = data['device_id']

        if device_id in onlineSeniorsDict:
            with onlineSeniorsDict as online_seniors:
                online_seniors[device_id]["time"] = data["time"]  # Assign new unix time
                online_seniors[device_id]["battery"] = data["battery"]
        else:  # New Device
            device_id = data.get("device_id")
            senior = Senior.objects.get(device_id=device_id)
            data["name"] = senior.name
            data["room_no"] = senior.room_no
            data["device_type"] = senior.device_type
            data["gender"] = senior.gender
            data["data"] = [{"value": 0, "time": 0}]  # Create list to store sensor data

            with onlineSeniorsDict as online_seniors:
                online_seniors[device_id] = data

        # if device_id in onlineSeniorsDict:
        #     with onlineSeniorsDict as online_seniors:
        #         data2 = copy.deepcopy(data_r)
        #         data2.pop("device_id")
        #         online_seniors[device_id]["data"].append(data2)

        #         # Maintain fixed size
        #         if len(online_seniors[device_id]["data"]) > MAX_DATA_ARRAY_LEN:
        #             online_seniors[device_id]["data"].pop(0)

        # if dataMedium.senior_exist(text_data['device_id']) is False:

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                "type": 'send_message_to_frontend',
                "message": text_data
            }
        )

    def send_message_to_frontend(self,event):
        print("EVENT TRIGERED")
        # Receive message from room group
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))