# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat, Message
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#         self.chat_group_name = f'chat_{self.chat_id}'

#         # Подключаемся к группе чата
#         await self.channel_layer.group_add(
#             self.chat_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Отключаемся от группы
#         await self.channel_layer.group_discard(
#             self.chat_group_name,
#             self.channel_name
#         )

#     # При получении сообщения с WebSocket
#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)
#             message = data['message']
#             sender_id = self.scope["user"].id
#         except json.JSONDecodeError:
#             await self.send(text_data=json.dumps({
#                 'error': 'Invalid JSON'
#             }))

#         # Сохраняем сообщение в БД
#         await self.save_message(sender_id, self.chat_id, message)

#         # Рассылаем сообщение всем в группе
#         await self.channel_layer.group_send(
#             self.chat_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender_id': sender_id,
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender_id': event['sender_id'],
#         }))

#     @database_sync_to_async
#     def save_message(self, sender_id, chat_id, message):
#         sender = User.objects.get(id=sender_id)
#         chat = Chat.objects.get(id=chat_id)
#         return Message.objects.create(chat=chat, sender=sender, content=message)


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat, Message
# from django.contrib.auth import get_user_model
# import logging

# logger = logging.getLogger(__name__)

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         user = self.scope["user"]
#         if not user.is_authenticated:
#             logger.warning("Unauthenticated user tried to connect.")
#             await self.close()
#             return
#         # if not user.is_authenticated:
#         #     await self.close()
#         #     return

#         self.receiver_id = int(self.scope['url_route']['kwargs']['receiver_id'])
#         self.receiver = await self.get_user(self.receiver_id)
#         if not self.receiver:
#             logger.warning(f"Receiver with ID {self.receiver_id} does not exist.")
#             await self.close()
#             return
#         # if not self.receiver:
#         #     await self.close()
#         #     return

#         self.chat = await self.get_or_create_chat(user, self.receiver)
#         self.chat_group_name = f'chat_{self.chat.id}'

#         await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         if hasattr(self, 'chat_group_name'):
#             await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)


#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)
#             message = data.get('message')
#             if not message:
#                 return
#         except json.JSONDecodeError:
#             await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))
#             return

#         sender = self.scope["user"]
#         msg_obj = await self.save_message(self.chat, sender, message)

#         await self.channel_layer.group_send(
#             self.chat_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': msg_obj.content,
#                 'sender_id': sender.id,
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender_id': event['sender_id'],
#         }))

#     @database_sync_to_async
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return None

#     @database_sync_to_async
#     def get_or_create_chat(self, user1, user2):
#         chat = Chat.objects.filter(participants=user1).filter(participants=user2).first()
#         if chat:
#             return chat
#         chat = Chat.objects.create()
#         chat.participants.add(user1, user2)
#         return chat

#     @database_sync_to_async
#     def save_message(self, chat, sender, content):
#         return Message.objects.create(chat=chat, sender=sender, content=content)



# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat, Message
# from django.contrib.auth import get_user_model
# from django.db.models import Count

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     # async def connect(self):
#     #     self.user = self.scope["user"]
#     #     if not self.user.is_authenticated:
#     #         await self.close()
#     #         return

#     #     # Временно ставим None — будет установлен при первом receive
#     #     self.chat = None
#     #     await self.accept()
#     @database_sync_to_async
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(id=int(user_id))
#         except User.DoesNotExist:
#             return None


#     async def connect(self):
#         self.user = self.scope["user"]
#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         try:
#             receiver_id = self.scope['url_route']['kwargs']['receiver_id']
#             self.receiver = await self.get_user(int(receiver_id))
#             if not self.receiver:
#                 await self.send(text_data=json.dumps({"error": "Receiver not found"}))
#                 await self.close()
#                 return

#             # Получаем или создаём чат
#             self.chat = await self.get_or_create_chat(int(self.user.id), int(self.receiver.id))
#             self.chat_group_name = f"chat_{self.chat.id}"

#             await self.channel_layer.group_add(
#                 self.chat_group_name,
#                 self.channel_name
#             )
#             await self.accept()

#         except KeyError:
#             await self.send(text_data=json.dumps({"error": "Missing receiver_id in URL"}))
#             await self.close()

#     async def disconnect(self, close_code):
#         if hasattr(self, 'chat_group_name'):
#             await self.channel_layer.group_discard(
#                 self.chat_group_name,
#                 self.channel_name
#             )

#     # async def receive(self, text_data):
#     #     try:
#     #         data = json.loads(text_data)
#     #         message = data["message"]
#     #         recipient_id = data["recipient_id"]
#     #     except (KeyError, json.JSONDecodeError):
#     #         await self.send(text_data=json.dumps({"error": "Invalid message format"}))
#     #         return

#     #     sender = self.scope["user"]

#     #     chat = await self.get_or_create_chat(sender.id, recipient_id)
#     #     self.chat = chat
#     #     self.chat_group_name = f"chat_{chat.id}"

#     #     # Подключение к группе (если не подключен)
#     #     await self.channel_layer.group_add(
#     #         self.chat_group_name,
#     #         self.channel_name
#     #     )

#     #     saved_message = await self.save_message(sender.id, chat.id, message)

#     #     # Рассылаем сообщение участникам группы
#     #     await self.channel_layer.group_send(
#     #         self.chat_group_name,
#     #         {
#     #             'type': 'chat_message',
#     #             'message': saved_message.content,
#     #             'sender_id': sender.id,
#     #         }
#     #     )

#     async def receive(self, text_data):
#         try:
#             data = json.loads(text_data)
#             message = data["message"]
#         except (KeyError, json.JSONDecodeError):
#             await self.send(text_data=json.dumps({"error": "Invalid message format"}))
#             return

#         saved_message = await self.save_message(int(self.user.id), int(self.chat.id), message)

#         await self.channel_layer.group_send(
#             self.chat_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': saved_message.content,
#                 'sender_id': int(self.user.id),
#             }
#         )


#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender_id': event['sender_id'],
#         }))

    

#     @database_sync_to_async
#     def get_or_create_chat(self, sender_id, recipient_id):
#         sender_id = int(sender_id)
#         recipient_id = int(recipient_id)
#         # Пытаемся найти чат, где оба пользователя являются участниками
#         chats = Chat.objects.annotate(num_participants=Count('participants')).filter(
#             participants__id=sender_id
#         ).filter(
#             participants__id=recipient_id
#         ).filter(
#             num_participants=2
#         )
#         if chats.exists():
#             return chats.first()

#         # Если не существует — создаём
#         chat = Chat.objects.create()
#         chat.participants.add(sender_id, recipient_id)
#         return chat

#     @database_sync_to_async
#     def save_message(self, sender_id, chat_id, message):
#         sender_id = int(sender_id)
#         chat_id = int(chat_id)
#         sender = User.objects.get(id=sender_id)
#         chat = Chat.objects.get(id=chat_id)
#         return Message.objects.create(chat=chat, sender=sender, content=message)



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
import pytz


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

    async def disconnect(self, close_code):
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
                'created_at': created_at_bishkek.strftime('%d.%m.%Y %H:%M')
            }
        )


    async def chat_message(self, event):
        # Если текущий пользователь отправил сообщение — имя будет "me"
        sender_name = "me" if self.user.id == event['sender_id'] else event['sender_name']

        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_name': sender_name,
            'created_at': event['created_at'],
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
