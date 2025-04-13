from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdvertisementCreateSerializer, AdvertisementShortListSerializer, AdvertisementFullRetrieveSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Advertisement, Complectation, OtherBenefits
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes, OpenApiParameter
from rest_framework.parsers import MultiPartParser


# @extend_schema(
#     request=AdvertisementCreateSerializer,
#     responses={status.HTTP_201_CREATED: AdvertisementCreateSerializer},
#     examples=[
#         OpenApiExample(
#             name="Создание объявления с JSON и файлами",
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
#                 "complectation": '{"leather": true, "xenon": true, "USB": true}',
#                 "other": '{"recently_imported": true, "tax_paid": true}',
#                 "images": ["/home/bagyshan/Pictures/Screenshots/Screenshot from 2024-09-05 14-10-25.png",
#                            "/home/bagyshan/Pictures/Screenshots/Screenshot from 2024-09-06 01-29-35.png" 
#                 ],
#                 "owner": 2
#             },
#             request_only=True,
#             media_type="multipart/form-data",
#         )
#     ]
# )
@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'mark': {'type': 'string', 'example': 'BMW'},
                'model': {'type': 'string', 'example': 'BMW_M3'},
                'year_of_manufacture': {'type': 'integer', 'example': 2024},
                'generation': {'type': 'integer', 'example': 23978803},
                'notice': {'type': 'string', 'example': 'седан'},
                'engine_type': {'type': 'string', 'example': 'бензин'},
                'drive': {'type': 'string', 'example': 'полный'},
                'transmission': {'type': 'string', 'example': 'автоматическая'},
                'modification': {'type': 'string', 'example': 'Competition'},
                'steering_wheel': {'type': 'string', 'example': 'Левый'},
                'color': {
                    'type': 'string',
                    'enum': ['#000000', '#C0C0C0', '#FFFFFF', '#808080', '#F5F5DC', '#30D5C8',
                             '#800000', '#CD7F32', '#DE3163', '#87CEEB', '#FFFF00', '#008000',
                             '#FFD700', '#A52A2A', '#FF0000', '#FFA500', '#FFC0CB', '#0000FF',
                             '#C8A2C8', '#800080', '#7FFFD4', '#580F41'],
                    'example': '#000000'
                },
                'state': {
                    'type': 'string',
                    'enum': ['good', 'great', 'bad', 'new'],
                    'example': 'good'
                },
                'mileage': {'type': 'integer', 'example': 100000},
                'units_of_mileage': {
                    'type': 'string',
                    'enum': ['km', 'mile'],
                    'example': 'km'
                },
                'availability_in_kyrgyzstan': {
                    'type': 'string',
                    'enum': ['yes', 'with order', 'in road'],
                    'example': 'yes'
                },
                'customs_in_kyrgyzstan': {'type': 'boolean', 'example': True},
                'urgently': {'type': 'boolean', 'example': False},
                'country_of_registration': {
                    'type': 'string',
                    'enum': ['kyrgyzstan', 'not registered'],
                    'example': 'kyrgyzstan'
                },
                'possibility_of_exchange': {
                    'type': 'string',
                    'enum': ['consider the options', 'with additional payment by the buyer',
                             'with seller surcharge', 'key to key', 'do not offer exchange',
                             'exchange for real estate', 'exchange only'],
                    'example': 'consider the options'
                },
                'possibility_of_installments': {'type': 'boolean', 'example': True},
                'currency': {
                    'type': 'string',
                    'enum': ['som', 'USD'],
                    'example': 'USD'
                },
                'price': {'type': 'integer', 'example': 12000},
                'region': {
                    'type': 'string',
                    'enum': ['chui', 'ik', 'talas', 'naryn', 'jalal-abad', 'osh', 'batken'],
                    'example': 'chui'
                },
                'city': {
                    'type': 'string',
                    'enum': ['bishkek', 'osh'],
                    'example': 'bishkek'
                },
                'permission_to_comment': {
                    'type': 'string',
                    'enum': ['nobody', 'authenticated'],
                    'example': 'authenticated'
                },
                'description': {'type': 'string', 'example': 'Автомобиль в отличном состоянии'},
                'phone_number': {'type': 'string', 'example': '+996700123456'},
                'complectation': {
                    'type': 'string',
                    'example': '{"ABS": true, "USB": true}'
                },
                'other': {
                    'type': 'string',
                    'example': '{"recently_imported": true, "tax_paid": true}'
                },
                'images': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'format': 'binary'
                    }
                },
                'owner': {'type': 'integer', 'example': 2}
            },
            'required': [
                'mark', 'model', 'year_of_manufacture', 'notice', 'engine_type',
                'drive', 'transmission', 'steering_wheel', 'color', 'state', 'mileage',
                'units_of_mileage', 'availability_in_kyrgyzstan', 'country_of_registration',
                'currency', 'price', 'region', 'city', 'phone_number', 'owner'
            ]
        }
    },
    responses={
        status.HTTP_201_CREATED: AdvertisementCreateSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT
    },
    examples=[
        OpenApiExample(
            "Создание объявления с JSON-полями и изображениями",
            value={
                "mark": "BMW",
                "model": "BMW_M3",
                "year_of_manufacture": 2024,
                "generation": 23978803,
                "notice": "седан",
                "engine_type": "бензин",
                "drive": "полный",
                "transmission": "автоматическая",
                "steering_wheel": "Левый",
                "color": "#000000",
                "state": "good",
                "mileage": 100000,
                "units_of_mileage": "km",
                "availability_in_kyrgyzstan": "yes",
                "customs_in_kyrgyzstan": True,
                "country_of_registration": "kyrgyzstan",
                "currency": "USD",
                "price": 12000,
                "region": "chui",
                "city": "bishkek",
                "phone_number": "+996700123456",
                "complectation": '{"ABS": true, "USB": true}',
                "other": '{"recently_imported": true, "tax_paid": true}',
                "owner": 2
            },
            request_only=True
        )
    ],
    tags=['Advertisement create']
)
class AdvertisementCreateView(APIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = AdvertisementCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdvertisementGetViewSet(ReadOnlyModelViewSet):
    queryset = Advertisement.objects.all().select_related('complectation', 'other').prefetch_related('images')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdvertisementFullRetrieveSerializer
        return AdvertisementShortListSerializer
    

class AdvertisementMetaInfoView(APIView):
    def get(self, request):
        field_info = {
            field.name: str(field.verbose_name)
            for field in Advertisement._meta.fields
        }
        return Response(field_info)
    
class ComplectationMetaInfoView(APIView):
    def get(self, request):
        field_info = {
            field.name: str(field.verbose_name)
            for field in Complectation._meta.fields
        }
        return Response(field_info)
    
class OtherBenefitsMetaInfoView(APIView):
    def get(self, request):
        field_info = {
            field.name: str(field.verbose_name)
            for field in OtherBenefits._meta.fields
        }
        return Response(field_info)
    