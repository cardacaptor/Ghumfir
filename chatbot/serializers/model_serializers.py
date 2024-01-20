from rest_framework import serializers

from chatbot.models import ChatMessage, MessagePost
from feed.model_serializers.post_serializer import PostSerializer

class MessagePostSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=False)
    
    class Meta: 
        model = MessagePost
        fields = ['post']

class ChatMessageSerializer(serializers.ModelSerializer):
    posts = MessagePostSerializer(many=True)
    
    class Meta:
        model = ChatMessage
        fields = ['posts', 'isBotMessage', 'message', 'created']
        
        