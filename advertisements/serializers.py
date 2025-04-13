import json
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
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

# @extend_schema_serializer(
#     examples=[
#         OpenApiExample(
#             'Пример объявления',
#             value={
#                 'mark': 'BMW',
#                 'model': 'BMW_M3',
#                 'year_of_manufacture': 2024,
#                 'generation': 7,
#                 'notice': 'седан',
#                 'engine_type': 'бензин',
#                 'drive': 'передний',
#                 'transmission': 'автомат',
#                 'modification': '2.5L',
#                 'steering_wheel': 'левый',
#                 'color': '#000000',
#                 'state': 'good',
#                 'mileage': 100000,
#                 'units_of_mileage': 'км',
#                 'availability_in_kyrgyzstan': 'yes',
#                 'customs_in_kyrgyzstan': True,
#                 'urgently': False,
#                 'country_of_registration': 'kyrgyzstan',
#                 'possibility_of_exchange': 'key to key',
#                 'possibility_of_installments': False,
#                 'currency': 'USD',
#                 'price': 15000,
#                 'region': 'chui',
#                 'city': 'bishkek',
#                 'permission_to_comment': 'authenticated',
#                 'description': 'Очень хорошее авто в идеальном состоянии.',
#                 'phone_number': '+996700123456',
#             },
#             request_only=True
#         )
#     ]
# )
# @extend_schema_serializer(
#     examples=[
#         OpenApiExample(
#             name='Пример объявления',
#             value={
#                 "mark": "BMW",
#                 "model": "BMW_M3",
#                 "year_of_manufacture": 2024,
#                 "generation": 23978803,
#                 "notice": "седан",
#                 "engine_type": "бензин",
#                 "drive": "полный",
#                 "transmission": "автоматическая",
#                 "modification": "Competition",
#                 "steering_wheel": "Левый",
#                 "color": "#000000",
#                 "state": "new",
#                 "mileage": 10000,
#                 "units_of_mileage": "км",
#                 "availability_in_kyrgyzstan": "yes",
#                 "customs_in_kyrgyzstan": True,
#                 "urgently": False,
#                 "country_of_registration": "kyrgyzstan",
#                 "possibility_of_exchange": "key to key",
#                 "possibility_of_installments": True,
#                 "currency": "USD",
#                 "price": 50000,
#                 "region": "chui",
#                 "city": "bishkek",
#                 "permission_to_comment": "authenticated",
#                 "description": "Отличное состояние",
#                 "phone_number": "+996700123456",
#                 "complectation": {
#                     "leather": True,
#                     "xenon": True,
#                     "USB": True
#                 },
#                 "other": {
#                     "recently_imported": True,
#                     "tax_paid": True
#                 },
#                 "images": ["/home/bagyshan/Pictures/Screenshots/Screenshot from 2024-09-05 14-10-25.png",
#                            "/home/bagyshan/Pictures/Screenshots/Screenshot from 2024-09-06 01-29-35.png" 
#                 ],
#                 "owner": 2
#             },
#             request_only=True,
#             response_only=False
#         )
#     ]
# )
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
        # images_data = self.context['request'].FILES.getlist('images') # <------------
        images_data = validated_data.pop('images', None) or self.context['request'].FILES.getlist('images')

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
