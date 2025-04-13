from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.AdvertisementGetViewSet)

urlpatterns = [
    path("", views.AdvertisementCreateView.as_view()),
    path("get/", include(router.urls)),
    path("advertisement-metainfo/", views.AdvertisementMetaInfoView.as_view()),
    path("complectation-metainfo/", views.ComplectationMetaInfoView.as_view()),
    path("other-benefits-metainfo/", views.OtherBenefitsMetaInfoView.as_view())
]
