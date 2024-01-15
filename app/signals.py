from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from .models import Product, CityCountry

geolocator = Nominatim(user_agent="app")

@receiver(pre_save, sender=CityCountry)
def disconnect_signals(sender, instance, **kwargs):
    post_save.disconnect(generate_location, sender=CityCountry)

@receiver(post_save, sender=CityCountry)
def generate_location(sender, instance, **kwargs):
    location_string = f"{instance.city}, {instance.country}"
    
    try:
        location = geolocator.geocode(location_string)

        if location:
            instance.latitude = location.latitude
            instance.longitude = location.longitude
            instance.save()

            Product.objects.filter(location=instance).update(latitude=instance.latitude, longitude=instance.longitude)

    except Exception as e:
        print(f"Error geocoding: {e}")

@receiver(post_save, sender=CityCountry)
def reconnect_signals(sender, instance, **kwargs):
    post_save.connect(generate_location, sender=CityCountry)
