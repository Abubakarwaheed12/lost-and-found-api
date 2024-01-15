from django.db import models
from accounts.models import User


class CityCountry(models.Model):
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.city}, {self.country}"
    

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    item = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=[
            ('lost', 'Lost'), 
            ('found', 'Found')
            ],
        default=None,
        null=False  
    )
    category = models.CharField(max_length=255)
    date_added = models.DateField(default=None, null=True, blank=True)
    time_added = models.TimeField(default=None, null=True, blank=True)
    location = models.ForeignKey(CityCountry, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    description = models.TextField()

    def __str__(self):
        return self.item
