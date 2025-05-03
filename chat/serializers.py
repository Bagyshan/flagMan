from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_login', 'avatar', 'is_company']

class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'created_at']

    def create(self, validated_data):
        request = self.context['request']
        chat = Chat.objects.create()
        chat.participants.add(request.user)
        other_users = validated_data.get('participants', [])
        for user in other_users:
            chat.participants.add(user)
        return chat

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['participants'] = UserSerializer(instance.participants.all(), many=True).data
        return rep

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'created_at']
        read_only_fields = ['sender', 'chat']