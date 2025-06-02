from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from drf_yasg import openapi

class ChatListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

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
        return Message.objects.filter(chat_id=chat_id).order_by('created_at')
    

    def list(self, request, *args, **kwargs):
        """
        Возвращает JSON вида:
        {
            "unread_messages": [ … ],
            "read_messages":   [ … ]
        }
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        all_data = serializer.data

        # Разбиваем на прочитанные и непрочитанные
        read_messages = [msg for msg in all_data if msg['is_read']]
        unread_messages = [msg for msg in all_data if not msg['is_read']]

        return Response({
            "unread_messages": unread_messages,
            "read_messages":   read_messages,
        })

    def perform_create(self, serializer):
        chat_id = self.kwargs['chat_id']
        serializer.save(chat_id=chat_id, sender=self.request.user)


class UnreadMessageCountAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
        unread_count = chat.messages.filter(is_read=False).exclude(sender=request.user).count()
        return Response({'unread_count': unread_count})


class ChatRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)



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