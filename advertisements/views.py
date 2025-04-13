from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdvertisementCreateSerializer, AdvertisementShortListSerializer, AdvertisementFullRetrieveSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Advertisement, Complectation, OtherBenefits

class AdvertisementCreateView(APIView):
    permission_classes = [IsAuthenticated]

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
    