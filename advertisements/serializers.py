import json
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Advertisement, AdvertisementImage, Complectation, OtherBenefits
from django.contrib.auth import get_user_model
from config.settings import CARS_BASE_TOKEN
import requests

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

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

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
        validated_data.pop("is_active", None)

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
        fields = ['id', 'name', 'last_login', 'avatar', 'is_company']

class AdvertisementFullRetrieveSerializer(serializers.ModelSerializer):
    complectation = ComplectationSerializer()
    other = OtherBenefitsSerializer()
    images = AdvertisementImageSerializer(many=True, read_only=True)
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Получаем значения mark и model
        mark = instance.mark
        model = instance.model
        generation_id = instance.generation

        try:
            url = f"https://cars-base.ru/api/cars/{mark}/{model}?key={CARS_BASE_TOKEN}"
            response = requests.get(url)

            if response.status_code == 200:
                generations = response.json()
                generation_info = next(
                    (gen for gen in generations if str(gen.get('id')) == str(generation_id)), None
                )

                if generation_info:
                    data['generation'] = generation_info
        except Exception as e:
            # Логируем или просто игнорируем ошибки
            print(f"Ошибка при получении поколения: {e}")

        return data
