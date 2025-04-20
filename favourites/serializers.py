from rest_framework import serializers
from advertisements.serializers import AdvertisementShortListSerializer
from .models import Favorite



class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementShortListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'advertisement', 'created_at']