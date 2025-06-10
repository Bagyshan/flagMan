import json
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Advertisement, AdvertisementImage, Complectation, OtherBenefits
from django.contrib.auth import get_user_model
from config.settings import CARS_BASE_TOKEN
from favourites.models import Favorite
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
        fields = ['id', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class AdvertisementCreateSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    deleted_images = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
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
    
    def update(self, instance, validated_data):
        request = self.context.get('request')

        complectation_data = validated_data.pop('complectation', None)
        other_data = validated_data.pop('other', None)
        images_data = validated_data.pop('images', None)
        deleted_images = validated_data.pop('deleted_images', [])

        # Удаление отдельных изображений по ID
        if deleted_images:
            AdvertisementImage.objects.filter(id__in=deleted_images, advertisement=instance).delete()

        # Добавление новых изображений
        if images_data:
            for image in images_data:
                AdvertisementImage.objects.create(advertisement=instance, image=image)

        # Обновляем complectation
        if complectation_data:
            if instance.complectation:
                for key, value in complectation_data.items():
                    setattr(instance.complectation, key, value)
                instance.complectation.save()
            else:
                complectation = Complectation.objects.create(**complectation_data)
                instance.complectation = complectation

        # Обновляем other
        if other_data:
            if instance.other:
                for key, value in other_data.items():
                    setattr(instance.other, key, value)
                instance.other.save()
            else:
                other = OtherBenefits.objects.create(**other_data)
                instance.other = other

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class AdvertisementShortListSerializer(serializers.ModelSerializer):
    is_favorite = serializers.SerializerMethodField()
    images = AdvertisementImageSerializer(many=True, read_only=True)

    # Русские отображения для choices
    color = serializers.SerializerMethodField()
    units_of_mileage = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
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
            'favorites_count',
            'views',
            'is_favorite',
            'created_at',
            'updated_at'
        ]
    

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, advertisement=obj).exists()
        return False

    def get_color(self, obj):
        return obj.get_color_display()

    def get_units_of_mileage(self, obj):
        return obj.get_units_of_mileage_display()

    def get_currency(self, obj):
        return obj.get_currency_display()

    def get_city(self, obj):
        return obj.get_city_display()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_login', 'avatar', 'is_company']

class AdvertisementFullRetrieveSerializer(serializers.ModelSerializer):
    complectation = ComplectationSerializer()
    other = OtherBenefitsSerializer()
    images = AdvertisementImageSerializer(many=True, read_only=True)
    owner = OwnerSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()

    # Отображение на русском
    color = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    units_of_mileage = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    availability_in_kyrgyzstan = serializers.SerializerMethodField()
    country_of_registration = serializers.SerializerMethodField()
    possibility_of_exchange = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    permission_to_comment = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = '__all__'

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, advertisement=obj).exists()
        return False

    def get_color(self, obj):
        return obj.get_color_display()

    def get_currency(self, obj):
        return obj.get_currency_display()

    def get_city(self, obj):
        return obj.get_city_display()

    def get_units_of_mileage(self, obj):
        return obj.get_units_of_mileage_display()

    def get_state(self, obj):
        return obj.get_state_display()

    def get_availability_in_kyrgyzstan(self, obj):
        return obj.get_availability_in_kyrgyzstan_display()

    def get_country_of_registration(self, obj):
        return obj.get_country_of_registration_display()

    def get_possibility_of_exchange(self, obj):
        return obj.get_possibility_of_exchange_display()

    def get_region(self, obj):
        return obj.get_region_display()

    def get_permission_to_comment(self, obj):
        return obj.get_permission_to_comment_display()
    
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
