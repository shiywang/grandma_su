from django.urls import re_path
from device_manager import SensorDataConsumer
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/sensordata/(?P<type>[-\w]+)', SensorDataConsumer.as_asgi()),
]
