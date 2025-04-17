import json
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Advertisement, AdvertisementImage, Complectation, OtherBenefits
from django.contrib.auth import get_user_model

User = get_user_model()

class ComplectationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complectation
        fields = '__all__'

class OtherBenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherBenefits
        fields = '__all__'

class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['image']

class AdvertisementCreateSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True
    )
    # images = AdvertisementImageSerializer(many=True, required=False, write_only=True)
    complectation = serializers.JSONField(required=False, write_only=True)
    other = serializers.JSONField(required=False, write_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['owner']


    def create(self, validated_data):
        request = self.context.get('request')
        complectation_data = validated_data.pop('complectation', None)
        other_data = validated_data.pop('other', None)
        images_data = validated_data.pop('images', None) or self.context['request'].FILES.getlist('images')

        complectation = Complectation.objects.create(**complectation_data) if complectation_data else None
        other = OtherBenefits.objects.create(**other_data) if other_data else None

        advertisement = Advertisement.objects.create(
            **validated_data,
            complectation=complectation,
            other=other,
            owner=request.user,
            is_active=True 
        )

        for image in images_data:
            AdvertisementImage.objects.create(advertisement=advertisement, image=image)

        return advertisement
    

class AdvertisementShortListSerializer(serializers.ModelSerializer):
    images = AdvertisementImageSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'mark',
            'model',
            'generation',
            'year_of_manufacture',
            'notice',
            'engine_type',
            'drive',
            'transmission',
            'steering_wheel',
            'color',
            'units_of_mileage',
            'mileage',
            'currency',
            'price',
            'city',
            'images',
            'created_at',
            'updated_at'
        ]


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_login']

class AdvertisementFullRetrieveSerializer(serializers.ModelSerializer):
    complectation = ComplectationSerializer()
    other = OtherBenefitsSerializer()
    images = AdvertisementImageSerializer(many=True, read_only=True)
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
