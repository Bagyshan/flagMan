from rest_framework.views import APIView
from rest_framework import generics, views
from rest_framework import viewsets, permissions, mixins
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdvertisementCreateSerializer, AdvertisementShortListSerializer, AdvertisementFullRetrieveSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Advertisement, Complectation, OtherBenefits
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiTypes, OpenApiParameter
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdvertisementFilter
from rest_framework.filters import OrderingFilter
from django.core.cache import cache


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
                    'enum': ['black', 'silver', 'white', 'grey', 'beige', 'turquoise',
                             'burgundy', 'bronze', 'cherry', 'white blue', 'yellow', 'green',
                             'gold', 'brown', 'red', 'orange', 'pink', 'blue',
                             'lilac', 'violet', 'chameleon', 'eggplant'],
                    'example': 'black'
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
                # 'owner': {'type': 'integer', 'example': 2}
            },
            'required': [
                'mark', 'model', 'year_of_manufacture', 'notice', 'engine_type',
                'drive', 'transmission', 'steering_wheel', 'color', 'state', 'mileage',
                'units_of_mileage', 'availability_in_kyrgyzstan', 'country_of_registration',
                'currency', 'price', 'region', 'city', 'phone_number'
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
    tags=['advertisement create']
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

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AdvertisementFilter  

    ordering_fields = ['price', 'created_at', 'year_of_manufacture', 'mileage']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdvertisementFullRetrieveSerializer
        return AdvertisementShortListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user if request.user.is_authenticated else None
        user_or_ip = user.id if user else self.get_client_ip(request)

        cache_key = f"viewed_{instance.id}_{user_or_ip}"

        if not cache.get(cache_key):
            instance.views += 1
            instance.save(update_fields=["views"])
            cache.set(cache_key, True, timeout=60 * 60 * 24)  # 24 часа

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '')
    

@extend_schema(
    tags=["advertisements edit"]
)
class AdvertisementUpdateDeleteViewSet(
    mixins.UpdateModelMixin,    # для PUT/PATCH
    mixins.DestroyModelMixin,   # для DELETE
    viewsets.GenericViewSet
):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementCreateSerializer  # Используется для create, update
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        # Возвращаем только объявления текущего пользователя
        return Advertisement.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        # Проверка, что пользователь владелец
        if self.get_object().owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого объявления.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете удалить это объявление.")
        instance.delete()
    

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
    

class AdvertisementChoicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "color": dict(Advertisement.COLOR_CHOICES),
            "state": dict(Advertisement.STATE_CHOICES),
            "availability_in_kyrgyzstan": dict(Advertisement.AVAILABILITY_IN_KYRGYZSTAN_CHOICES),
            "country_of_registration": dict(Advertisement.COUNTRY_OF_REGISTRATION_CHOICES),
            "possibility_of_exchange": dict(Advertisement.POSSIBILITY_OF_EXCHANGE_CHOICES),
            "currency": dict(Advertisement.CURRENCY_CHOICES),
            "region": dict(Advertisement.REGION_CHOICES),
            "city": dict(Advertisement.CITY_CHOICES),
            "permission_to_comment": dict(Advertisement.PERMISSION_TO_COMMENT_CHOICES),
            "units_of_mileage": dict(Advertisement.UNITS_OF_MILEAGE_CHOICES),
        })
    