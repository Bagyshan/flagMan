from django.db import models
from django.contrib.auth import get_user_model
from advertisements.models import Advertisement

# Create your models here.

User = get_user_model()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'advertisement')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"