from django.urls import path
from .views import FavoriteListView, ToggleFavoriteView

urlpatterns = [
    path('', FavoriteListView.as_view(), name='favorite-list'),
    path('toggle/<int:advertisement_id>/', ToggleFavoriteView.as_view(), name='favorite-toggle'),
]