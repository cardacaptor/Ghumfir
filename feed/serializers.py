
from rest_framework import serializers

from feed.models.post import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'caption', 'address', 'url', "latitude", "longitude"]

class Pagination(serializers.Serializer):
    page = serializers.IntegerField(default = 1)
    size = serializers.IntegerField(default = 10)
    liked =  serializers.IntegerField(default = 1)


class LikeActionSerializer(serializers.Serializer):
    postId = serializers.IntegerField()
