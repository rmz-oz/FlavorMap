from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Favorite
from restaurants.models import Restaurant

class FavoriteListView(LoginRequiredMixin, ListView):
    model = Favorite
    template_name = 'favorites/favorite_list.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
        if not created:
            fav.delete()
        return redirect('restaurant_detail', pk=restaurant.id)