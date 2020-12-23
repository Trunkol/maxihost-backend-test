from rest_framework import serializers
from survivor.models import Survivor
from django.contrib.gis.geos import Point

class SurvivorSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    latitude = serializers.DecimalField(required=True, decimal_places=3, max_digits=10)
    longitude = serializers.DecimalField(required=True, decimal_places=3, max_digits=10)
    created = serializers.DateTimeField(read_only=True)
    infected = serializers.BooleanField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Survivor
        exclude = ('localization', 'user')
    
    def create(self, validated_data):
        """
            Create and return a new `Survivor` instance, given the validated data.
        """
        if Survivor.objects.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError('This user already have a related survivor')
        
        latitude = float(validated_data.get('latitude', None))
        longitude = float(validated_data.get('longitude', None))
        
        validated_data['localization'] = Point(longitude, latitude)
        validated_data['user'] = self.context['request'].user
        survivor = Survivor.objects.create(**validated_data)
        
        return survivor

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
    
    