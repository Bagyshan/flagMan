from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Favorite
from .serializers import FavoriteSerializer
from advertisements.models import Advertisement
from django.db import models


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

class ToggleFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, advertisement_id):
        user = request.user
        try:
            ad = Advertisement.objects.get(id=advertisement_id)
        except Advertisement.DoesNotExist:
            return Response({'detail': 'Объявление не найдено'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=user, advertisement=ad)

        if not created:
            favorite.delete()
            ad.favorites_count = models.F('favorites_count') - 1
            ad.save(update_fields=['favorites_count'])
            return Response({'detail': 'Удалено из избранного'}, status=status.HTTP_200_OK)

        ad.favorites_count = models.F('favorites_count') + 1
        ad.save(update_fields=['favorites_count'])
        return Response({'detail': 'Добавлено в избранное'}, status=status.HTTP_201_CREATED)