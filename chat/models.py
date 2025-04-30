from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Chat(models.Model):
    participants = models.ManyToManyField(
        User,
        related_name='chats',
        verbose_name=_('Участники')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))

    def __str__(self):
        return f"Chat {self.id}"

class Message(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Чат')
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages_sent',
        verbose_name=_('Отправитель')
    )
    content = models.TextField(verbose_name=_('Текст сообщения'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата отправки'))
    is_read = models.BooleanField(default=False, verbose_name=_('Прочитано'))

    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"

    class Meta:
        ordering = ['created_at']  # Сообщения будут по порядку