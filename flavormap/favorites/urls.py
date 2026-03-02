from django.urls import path
from . import views

urlpatterns = [
    path('', views.FavoriteListView.as_view(), name='favorite_list'),
    path('toggle/<int:restaurant_id>/', views.FavoriteToggleView.as_view(), name='favorite_toggle'),
]