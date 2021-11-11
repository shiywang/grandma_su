from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


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

    def receive(self, text_data=None, bytes_data=None):
        print(" MESSAGE RECEIVED")
        # print(text_data)
        # data = json.loads(text_data)
        # message = data['message']
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