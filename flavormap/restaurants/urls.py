from django.urls import path
from . import views

urlpatterns = [
    path('', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurant/add/', views.RestaurantCreateView.as_view(), name='restaurant_add'),
    path('restaurant/<int:pk>/edit/', views.RestaurantUpdateView.as_view(), name='restaurant_edit'),
    path('restaurant/<int:pk>/delete/', views.RestaurantDeleteView.as_view(), name='restaurant_delete'),
]