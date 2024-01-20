from rest_framework import serializers
from chatbot.models import ChatMessage
from chatbot.validator import MessageValidatorBasic

class MessageSerializer(serializers.Serializer):
    validator = MessageValidatorBasic()
    message = serializers.CharField(validators = validator.chat_message_validator)
    
    def __str__(self):  
        return str({"message": self.message})
    
