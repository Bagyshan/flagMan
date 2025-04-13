import json
from rest_framework import serializers
from .models import Advertisement, AdvertisementImage, Complectation, OtherBenefits

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
    images = AdvertisementImageSerializer(many=True, required=False, write_only=True)
    complectation = serializers.JSONField(required=False, write_only=True)
    other = serializers.JSONField(required=False, write_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'

    # def to_internal_value(self, data):
    #     data = data.copy()

    #     # Распарсим строку JSON из multipart/form-data
    #     if isinstance(data.get('complectation'), str):
    #         try:
    #             data['complectation'] = json.loads(data['complectation'])
    #         except json.JSONDecodeError:
    #             raise serializers.ValidationError({'complectation': 'Неверный JSON'})

    #     if isinstance(data.get('other'), str):
    #         try:
    #             data['other'] = json.loads(data['other'])
    #         except json.JSONDecodeError:
    #             raise serializers.ValidationError({'other': 'Неверный JSON'})

    #     return super().to_internal_value(data)

    def create(self, validated_data):
        complectation_data = validated_data.pop('complectation', None)
        other_data = validated_data.pop('other', None)
        # images_data = validated_data.pop('images', [])
        images_data = self.context['request'].FILES.getlist('images')

        complectation = Complectation.objects.create(**complectation_data) if complectation_data else None
        other = OtherBenefits.objects.create(**other_data) if other_data else None

        advertisement = Advertisement.objects.create(
            **validated_data,
            complectation=complectation,
            other=other
        )

        # for image_data in images_data:
        #     AdvertisementImage.objects.create(advertisement=advertisement, image=image_data['image'])

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



class AdvertisementFullRetrieveSerializer(serializers.ModelSerializer):
    complectation = ComplectationSerializer()
    other = OtherBenefitsSerializer()
    images = AdvertisementImageSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
