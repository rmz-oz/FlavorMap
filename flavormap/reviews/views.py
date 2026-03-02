from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse
from .models import Review, ReviewLike
from restaurants.models import Restaurant

class ReviewCreateView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        with transaction.atomic():
            Review.objects.create(user=request.user, restaurant=restaurant, rating=rating, comment=comment)
        return redirect('restaurant_detail', pk=restaurant.id)

class ReviewReplyView(LoginRequiredMixin, View):
    def post(self, request, pk):
        parent = get_object_or_404(Review, id=pk)
        comment = request.POST.get('comment')
        with transaction.atomic():
            Review.objects.create(user=request.user, restaurant=parent.restaurant, rating=parent.rating, comment=comment, parent=parent)
        return redirect('restaurant_detail', pk=parent.restaurant.id)

class ReviewLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        value = request.POST.get('value') == 'true'
        like, created = ReviewLike.objects.get_or_create(user=request.user, review=review, defaults={'value': value})
        if not created:
            if like.value == value:
                like.delete()
            else:
                like.value = value
                like.save()
        return redirect('restaurant_detail', pk=review.restaurant.id)