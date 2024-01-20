from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from authentication.serializers.model_serializer import UserSerializer

class GetMeController(GenericAPIView): 
    permission_classes = [IsAuthenticated]
     
    def get(self, request, *args, **kwargs): 
        return Response({
                    "message": "Data load successful", 
                    "data": UserSerializer(request.user).data,
                    "status_code": 201
                    }, 
                status=201,
            )
