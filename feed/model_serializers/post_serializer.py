
from rest_framework import serializers
from feed.model_serializers.category_serializer import CategorySerializer
from feed.models.post import Post
from feed.model_serializers.post_action_serializer import PostActionSerializer, PostViewedSerializer
from feed.model_serializers.tag_serializer import PostTagSerializer


class PostSerializer(serializers.ModelSerializer):
    post_tags = PostTagSerializer(many=True)
    views = PostViewedSerializer(many=True)
    actions = PostActionSerializer(many=True)
    category = CategorySerializer()
    
    class Meta:
        model = Post
        fields = ['id','category', 'caption', 'url', 'price', "duration", "number_of_likes", "number_of_dislikes", "number_of_views", 'post_tags', 'actions', 'views']
