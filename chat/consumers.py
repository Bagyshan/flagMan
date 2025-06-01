import jwt
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from urllib.parse import parse_qs
from chat.models import Chat, Message
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.backends import TokenBackend
from django.utils.timezone import localtime
from accounts.tasks import send_fcm_notification_task
import pytz

from django.db.models import Q

KZ_TZ = pytz.timezone('Asia/Bishkek')

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.token = parse_qs(self.scope['query_string'].decode('utf-8')).get('token', [None])[0]

        self.user = await self.get_user_from_token(self.token)
        if not self.user:
            print("❌ Невалидный токен, закрытие соединения")
            await self.close()
            return

        if not await self.user_in_chat(self.user, self.chat_id):
            print(f"❌ Пользователь {self.user} не в чате {self.chat_id}")
            await self.close()
            return

        self.room_group_name = f'chat_{self.chat_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # 1) Пометить ВСЕ чужие непрочитанные сообщения как прочитанные
        read_ids = await self.mark_messages_as_read()

        # 2) Сообщить другой стороне, какие ID сообщений стали прочитанными
        if read_ids:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'messages_read',
                    'reader_id': self.user.id,
                    'message_ids': read_ids,
                }
            )

    async def disconnect(self, close_code):
        # Когда фронтенд делает socket.close(), сюда попадёт событие
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)  # 👈 разбираем JSON
        message_text = data.get('message') 

        if not message_text:
            return
        
        message_obj = await self.save_message(self.chat_id, self.user, message_text)
        created_at_bishkek = localtime(message_obj.created_at, timezone=KZ_TZ)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_obj.content,
                'sender': self.user.email,
                'sender_id': self.user.id,
                'sender_name': self.user.name,
                'created_at': created_at_bishkek.strftime('%d.%m.%Y %H:%M'),
                'message_id': message_obj.id,
                'is_read': message_obj.is_read,  # false сразу после создания
            }
        )


    async def chat_message(self, event):
        """
        Событие при получении нового сообщения.
        event содержит: message, sender, sender_id, sender_name, created_at, message_id, is_read
        """
        sender_name = "me" if self.user.id == event['sender_id'] else event['sender_name']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender':  event['sender'],
            'sender_name': sender_name,
            'created_at': event['created_at'],
            'message_id': event['message_id'],
            'is_read': event['is_read'],
        }))

    async def messages_read(self, event):
        """
        Реакция, когда кто-то из участников пометил сообщения как прочитанные.
        event содержит: reader_id, message_ids
        """
        # Если кто-то из нас — другой участник, просто пробрасываем событие на фронтенд.
        # Фронтенд узнает, что сообщения с id в 'message_ids' теперь is_read = true.
        if event['reader_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'messages_read',
                'reader_id': event['reader_id'],
                'message_ids': event['message_ids'],
            }))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            token_backend = TokenBackend(
                algorithm='HS256',
                signing_key=settings.SECRET_KEY 
            )
            valid_data = token_backend.decode(token, verify=True)
            user_id = valid_data['user_id']
            return User.objects.get(id=user_id)
        except (TokenError, InvalidToken, User.DoesNotExist):
            return None

    @database_sync_to_async
    def user_in_chat(self, user, chat_id):
        return Chat.objects.filter(id=chat_id, participants=user).exists()

    @database_sync_to_async
    def save_message(self, chat_id, user, content):
        chat = Chat.objects.get(id=chat_id)
        return Message.objects.create(chat=chat, sender=user, content=content)

    @database_sync_to_async
    def mark_messages_as_read(self):
        """
        Помечает все чужие непрочитанные сообщения в этом чате как прочитанные
        Возвращает список ID тех сообщений, у которых is_read изменился с False → True
        """
        # Получаем все релевантные непрочитанные
        unread_qs = Message.objects.filter(
            chat_id=self.chat_id,
            is_read=False
        ).exclude(sender=self.user)

        # Забираем их ID
        unread_ids = list(unread_qs.values_list('id', flat=True))
        if not unread_ids:
            return []

        # Делаем bulk update
        unread_qs.update(is_read=True)
        return unread_ids
