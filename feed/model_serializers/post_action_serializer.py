
from rest_framework import serializers
from authentication.serializers.model_serializer import UserSerializer
from feed.models.post_action import PostAction
from feed.models.post_viewed import PostViewed


class PostViewedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PostViewed
        fields = ['user', 'session_id']
        
        
class PostActionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = PostAction
        fields = ['user', 'action']
 