from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:restaurant_id>/', views.ReviewCreateView.as_view(), name='review_add'),
    path('reply/<int:pk>/', views.ReviewReplyView.as_view(), name='review_reply'),
    path('like/<int:pk>/', views.ReviewLikeToggleView.as_view(), name='review_like'),
]