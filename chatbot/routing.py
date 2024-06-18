from django.urls import re_path
from . import consumers

websocket_urlpatterns =[
    re_path(r"wss/chat/(?P<session_id>\w+)/$", consumers.ChatConsumer.as_asgi()),
]