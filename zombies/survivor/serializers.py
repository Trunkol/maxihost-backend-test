from rest_framework import serializers
from survivor.models import Survivor
from django.contrib.gis.geos import Point

class SurvivorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    infected = serializers.BooleanField(required=False)
    latitude = serializers.DecimalField(required=True, decimal_places=3, max_digits=10)
    longitude = serializers.DecimalField(required=True, decimal_places=3, max_digits=10)
    created = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Survivor

    def create(self, validated_data):
        """
            Create and return a new `Survivor` instance, given the validated data.
        """
        validated_data['localization'] = Point(float(validated_data['longitude']), 
                                                float(validated_data['latitude']))
        return Survivor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
            Update and return an existing `Survivor` instance, given the validated data.
        """
        latitude = validated_data.get('latitude', instance.latitude)
        longitude = validated_data.get('longitude', instance.longitude)

        instance.name = validated_data.get('name', instance.name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.latitude = latitude
        instance.longitude = longitude
        instance.localization = Point(float(longitude), float(latitude))
        instance.save()
        return instance
    