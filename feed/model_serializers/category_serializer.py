
from rest_framework import serializers

from feed.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'caption', 'url', 'number_of_destinations']