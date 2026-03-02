from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    PRICE_CHOICES = [('€','Cheap'),('€€','Moderate'),('€€€','Expensive')]
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    price_range = models.CharField(max_length=3, choices=PRICE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_restaurants')
    opening_hours = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        return self.reviews.aggregate(avg=models.Avg('rating'))['avg'] or 0

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='restaurant_photos/')
    caption = models.CharField(max_length=255, blank=True)