from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework.permissions import *
from chatbot.models import ChatMessage
from chatbot.serializers.model_serializers import ChatMessageSerializer
from chatbot.serializers.serializers import MessageSerializer

from ghumfir.serializers.pagination_serializer import Pagination
from ghumfir.utils.exceptions import MyValidationError
from ghumfir.wsgi import recommendation
from datetime import date

class ChatController(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        pagination  = Pagination(data = kwargs)
        isValid = pagination.is_valid()
        if isValid:
            size = 10
            start = (pagination.data["page"] - 1) * size
            end = start + size
            messages = ChatMessage.objects.filter(user_id = request.user.id).order_by('-created')[start:end]
            paginated_messages = ChatMessageSerializer(messages, many = True).data
            return Response({
                            "data": {
                                "messages": paginated_messages
                            }, 
                            "status_code": 201,
                            "message": "Chat successfully loaded",
                            },
                            status= 201
                            )
        raise MyValidationError(pagination.errors)