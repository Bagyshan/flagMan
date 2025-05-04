from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model
from django.db import models

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


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at']

    # def create(self, validated_data):
    #     request = self.context['request']
    #     chat = Chat.objects.create()
    #     chat.participants.add(request.user)
    #     other_users = validated_data.get('participants', [])
    #     for user in other_users:
    #         chat.participants.add(user)
    #     return chat

    def create(self, validated_data):
        request_user = self.context['request'].user
        other_users = validated_data.get('participants', [])

        if len(other_users) != 1:
            raise serializers.ValidationError("Chat must be between exactly two users.")

        other_user = other_users[0]
        desired_ids = {request_user.id, other_user.id}

        # Получаем все чаты с двумя участниками
        existing_chats = Chat.objects.annotate(
            num_participants=models.Count('participants')
        ).filter(num_participants=2)

        # Перебираем и сравниваем точный набор участников
        for chat in existing_chats:
            chat_user_ids = set(chat.participants.values_list('id', flat=True))
            if chat_user_ids == desired_ids:
                return chat

        # Если не найден — создаем новый
        chat = Chat.objects.create()
        chat.participants.add(request_user, other_user)
        return chat

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['participants'] = UserSerializer(instance.participants.all(), many=True, context=self.context).data
        return rep
    

class MessageByUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='sender.name')

    class Meta:
        model = Message
        fields = ['id', 'name', 'created_at', 'content']

class ParticipantWithMessagesSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'avatar', 'message']

    def get_message(self, user):
        chat = self.context.get('chat')
        messages = chat.messages.filter(sender=user)
        return MessageByUserSerializer(messages, many=True).data
    
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
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'created_at']
        read_only_fields = ['sender', 'chat']