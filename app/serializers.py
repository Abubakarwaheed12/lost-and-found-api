from rest_framework import serializers
from .models import Product,  CityCountry

class CityCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityCountry
        fields = ['id', 'city', 'country', 'latitude', 'longitude']


class ProductSerializer(serializers.ModelSerializer):
    location = CityCountrySerializer()
    class Meta:
        model = Product
        extra_kwargs = {
            'date_added': {'required': False},
            'time_added': {'required': False},
        }
        fields = '__all__'

    def create(self, validated_data):
        location_data = validated_data.pop('location', None)

        location_instance = CityCountry.objects.filter(
            city=location_data['city'], country=location_data['country']
        ).first()

        if not location_instance:
            location_instance = CityCountry.objects.create(**location_data)

        validated_data['location'] = location_instance
        return super().create(validated_data)
