from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model
from django.db import models
import pytz
from django.utils.timezone import localtime


KZ_TZ = pytz.timezone('Asia/Bishkek')

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'last_login', 'avatar', 'is_company']

    def get_avatar(self, obj):
        request = self.context.get('request')
        if not request or not obj.avatar:
            return None
        return request.build_absolute_uri(obj.avatar.url)


# class ChatSerializer(serializers.ModelSerializer):
#     participants = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), many=True, required=False
#     )

#     class Meta:
#         model = Chat
#         fields = ['id', 'participants', 'created_at']

#     # def create(self, validated_data):
#     #     request = self.context['request']
#     #     chat = Chat.objects.create()
#     #     chat.participants.add(request.user)
#     #     other_users = validated_data.get('participants', [])
#     #     for user in other_users:
#     #         chat.participants.add(user)
#     #     return chat

#     def create(self, validated_data):
#         request_user = self.context['request'].user
#         other_users = validated_data.get('participants', [])

#         if len(other_users) != 1:
#             raise serializers.ValidationError("Chat must be between exactly two users.")

#         other_user = other_users[0]
#         desired_ids = {request_user.id, other_user.id}

#         # Получаем все чаты с двумя участниками
#         existing_chats = Chat.objects.annotate(
#             num_participants=models.Count('participants')
#         ).filter(num_participants=2)

#         # Перебираем и сравниваем точный набор участников
#         for chat in existing_chats:
#             chat_user_ids = set(chat.participants.values_list('id', flat=True))
#             if chat_user_ids == desired_ids:
#                 return chat

#         # Если не найден — создаем новый
#         chat = Chat.objects.create()
#         chat.participants.add(request_user, other_user)
#         return chat

#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         rep['participants'] = UserSerializer(instance.participants.all(), many=True, context=self.context).data
#         return rep
    
# class ChatSerializer(serializers.ModelSerializer):
#     participants = serializers.SerializerMethodField()

#     class Meta:
#         model = Chat
#         fields = ['id', 'participants', 'created_at']

#     def get_participants(self, obj):
#         request_user = self.context['request'].user
#         other_users = obj.participants.exclude(id=request_user.id)
#         return UserSerializer(other_users, many=True, context=self.context).data

#     def create(self, validated_data):
#         request_user = self.context['request'].user
#         other_users = validated_data.get('participants', [])

#         if len(other_users) != 1:
#             raise serializers.ValidationError("Chat must be between exactly two users.")

#         other_user = other_users[0]
#         desired_ids = {request_user.id, other_user.id}

#         existing_chats = Chat.objects.annotate(
#             num_participants=models.Count('participants')
#         ).filter(num_participants=2)

#         for chat in existing_chats:
#             chat_user_ids = set(chat.participants.values_list('id', flat=True))
#             if chat_user_ids == desired_ids:
#                 return chat

#         chat = Chat.objects.create()
#         chat.participants.add(request_user, other_user)
#         return chat


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )
    participants_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'participants_info', 'created_at']

    def get_participants_info(self, obj):
        request_user = self.context['request'].user
        other_users = obj.participants.exclude(id=request_user.id)
        return UserSerializer(other_users, many=True, context=self.context).data

    def create(self, validated_data):
        request_user = self.context['request'].user
        other_users = validated_data.get('participants', [])

        if not isinstance(other_users, list) or len(other_users) != 1:
            raise serializers.ValidationError("Chat must be between exactly two users.")

        other_user = other_users[0]
        desired_ids = {request_user.id, other_user.id}

        # Ищем чат с теми же двумя участниками
        existing_chats = Chat.objects.annotate(num_participants=models.Count('participants')).filter(num_participants=2)

        for chat in existing_chats:
            chat_user_ids = set(chat.participants.values_list('id', flat=True))
            if chat_user_ids == desired_ids:
                return chat

        # Если не найден — создаём новый
        chat = Chat.objects.create()
        chat.participants.add(request_user, other_user)
        return chat

class MessageByUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'name', 'created_at', 'content']

    def get_name(self, obj):
        request = self.context.get('request')
        if request and obj.sender == request.user:
            return "me"
        return obj.sender.name

class ParticipantWithMessagesSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'avatar', 'is_company', 'last_login', 'message']

    def get_name(self, obj):
        request = self.context.get('request')
        if request and obj == request.user:
            return "me"
        return obj.name

    def get_message(self, user):
        chat = self.context.get('chat')
        request = self.context.get('request')
        messages = chat.messages.filter(sender=user)
        return MessageByUserSerializer(messages, many=True, context={'request': request}).data

    
    def get_avatar(self, obj):
        request = self.context.get('request')
        if not request or not obj.avatar:
            return None
        return request.build_absolute_uri(obj.avatar.url)

    
class ChatDetailSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['participants']

    def get_participants(self, chat):
        participants = chat.participants.all()
        return ParticipantWithMessagesSerializer(
            participants,
            many=True,
            context={'chat': chat, 'request': self.context.get('request')}
        ).data

class MessageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'name', 'content', 'created_at']
        read_only_fields = ['sender', 'chat']

    def get_name(self, obj):
        return obj.sender.name or obj.sender.email

    def get_created_at(self, obj):
        created_at_bishkek = localtime(obj.created_at, timezone=KZ_TZ)
        return created_at_bishkek.strftime('%d.%m.%Y %H:%M')