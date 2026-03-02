from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Restaurant
from django.db.models import Avg

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        category = self.request.GET.get('category')
        city = self.request.GET.get('city')
        price = self.request.GET.get('price')
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if city:
            queryset = queryset.filter(city__iexact=city)
        if price:
            queryset = queryset.filter(price_range=price)
        return queryset.order_by('-created_at')

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/restaurant_detail.html'
    context_object_name = 'restaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.object

        # Use related_name instead of importing Review
        context['reviews'] = restaurant.reviews.filter(parent__isnull=True).order_by('-created_at')

        if self.request.user.is_authenticated:
            context['favorite'] = restaurant.favorite_set.filter(user=self.request.user).exists()

        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()
        context['reviews'] = restaurant.reviews.filter(parent__isnull=True).order_by('-created_at')
        if self.request.user.is_authenticated:
            context['favorite'] = restaurant.favorite_set.filter(
                user=self.request.user
            ).exists()

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    fields = ['name','description','address','city','district','phone','price_range','category','opening_hours']
    template_name = 'restaurants/restaurant_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RestaurantUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Restaurant
    fields = ['name','description','address','city','district','phone','price_range','category','opening_hours']
    template_name = 'restaurants/restaurant_form.html'

class RestaurantDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Restaurant
    template_name = 'restaurants/restaurant_confirm_delete.html'
    success_url = reverse_lazy('restaurant_list')