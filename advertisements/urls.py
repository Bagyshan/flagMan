from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("get", views.AdvertisementGetViewSet)
router.register('edit', views.AdvertisementUpdateDeleteViewSet, basename='my-advertisement')

urlpatterns = [
    path("", views.AdvertisementCreateView.as_view()),
    path("", include(router.urls)),
    path("advertisement-metainfo/", views.AdvertisementMetaInfoView.as_view()),
    path("complectation-metainfo/", views.ComplectationMetaInfoView.as_view()),
    path("other-benefits-metainfo/", views.OtherBenefitsMetaInfoView.as_view())
]
