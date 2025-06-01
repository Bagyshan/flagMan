from django.urls import path
from .views import ChatListCreateAPIView, MessageListCreateAPIView, WebSocketInfoAPIView, ChatRetrieveAPIView, UnreadMessageCountAPIView

urlpatterns = [
    path('chats/', ChatListCreateAPIView.as_view(), name='chat-list-create'),
    path('chats/<int:chat_id>/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('chats/<int:chat_id>/unread_count/', UnreadMessageCountAPIView.as_view(),  name='chat-unread-count'),
    path('chats/<int:pk>/details', ChatRetrieveAPIView.as_view(), name='chat-detail'),
    path('websocket-info/', WebSocketInfoAPIView.as_view(), name='websocket-info'),
]