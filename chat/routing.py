# from django.urls import path
# from . import consumers

# # websocket_urlpatterns = [
# #     path('ws/chat/<str:chat_id>/', consumers.ChatConsumer.as_asgi()),
# # ]

# from django.urls import re_path

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<receiver_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
# ]

from django.urls import re_path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),
]