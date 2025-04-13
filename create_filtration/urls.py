from django.urls import path
from . import views

urlpatterns = [
    path("marks-list/", views.CarMarksAPIView.as_view()),
    path("models-list/", views.CarModelsAPIView.as_view()),
    path("generations-list/", views.CarGenerationsAPIView.as_view()),
    path("configurations/", views.CarOtherConfigurationsAPIView.as_view()),
    # path("notice-list/", views.CarNoticeListAPIView.as_view()),
    path("year-list/", views.CarYearAPIView.as_view()),
    # path("steering-wheels-list/", views.CarSteeringWheelsListAPIView.as_view()),
    # path("engine-type-list/", views.CarEngineTypeListAPIView.as_view()),
    # path("transmission-list/", views.CarTransmissionListAPIView.as_view()),
    # path("drive-list/", views.CarDriveListAPIView.as_view()),
    # path("modification-name-list/", views.CarModificationNameListAPIView.as_view())
]
