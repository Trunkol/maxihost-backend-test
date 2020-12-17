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

    '''
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
    '''