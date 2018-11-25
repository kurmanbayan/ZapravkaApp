from rest_framework import serializers
from .models import City, Station, Comment, Feature


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=200)  
    class Meta:
        model = Comment
        fields = "__all__"

class FeatureSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Feature
        fields = "__all__"
