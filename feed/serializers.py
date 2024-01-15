
from rest_framework import serializers

from feed.models.post import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'caption', 'url', 'price', "duration", "number_of_likes", "number_of_dislikes", "number_of_views"]

class Pagination(serializers.Serializer):
    page = serializers.IntegerField(default = 1)
    size = serializers.IntegerField(default = 10)

class PaginationWithSearch(serializers.Serializer):
    page = serializers.IntegerField(default = 1)
    size = serializers.IntegerField(default = 10)
    search = serializers.CharField()

class PostActionSerializer(serializers.Serializer):
    postId = serializers.IntegerField()
