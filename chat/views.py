from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ChatListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Текущий пользователь будет добавлен в serializer.create()
        serializer.save()

    # def perform_create(self, serializer):
    #     chat = serializer.save()
    #     chat.participants.add(self.request.user)

class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return Message.objects.filter(chat_id=chat_id)

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        serializer.save(chat_id=chat_id, sender=self.request.user)


class WebSocketInfoAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Инструкция по подключению к WebSocket для чата.",
        responses={200: openapi.Response(description="Описание WebSocket подключения")},
    )
    def get(self, request):
        return Response({
            "websocket_url": "ws://yourdomain.com/ws/chat/{chat_id}/",
            "send_format": {"message": "string"},
            "receive_format": {"message": "string", "sender_id": "int"}
        })