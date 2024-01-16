
from rest_framework import serializers

from feed.models.post import PostTag, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['key']

class PostTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    class Meta:
        model = PostTag
        fields = ['tag', 'value']