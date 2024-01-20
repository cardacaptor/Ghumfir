from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *
from chatbot.models import ChatMessage, MessagePost
from chatbot.serializers.model_serializers import ChatMessageSerializer
from chatbot.serializers.serializers import MessageSerializer

from ghumfir.utils.exceptions import MyValidationError
from ghumfir.wsgi import recommendation
from datetime import datetime

class SendTextController(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    
    def post(self, request, *args, **kwargs):
        req_message  = MessageSerializer(data = request.data)
        isValid = req_message.is_valid()
        if isValid:
            chat_message = ChatMessage(message = req_message.data["message"], user = request.user, isBotMessage = False)
            chat_message.save()
            (message, posts) = recommendation.get_post_based_on_message(req_message.data["message"], request.user.username)
            bot_message = ChatMessage(message = message, user = request.user, isBotMessage = True)
            bot_message.save()
            if(posts != None):
                MessagePost.objects.bulk_create(
                    [MessagePost(message_id = bot_message.id, post_id = i.id) for i in posts]
                )
            return Response({
                            "data": {
                                "reply": ChatMessageSerializer(bot_message).data
                            }, 
                            "status_code": 201,
                            "message": "Message sent successfully",
                            },
                            status= 200
                            )
        raise MyValidationError(message.errors)
