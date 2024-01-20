
from django.contrib.auth import *
from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from authentication.serializers.model_serializer import UserSerializer

from rest_framework.authtoken.models import Token
from authentication.serializers.serializers import SignUpSerializer
from ghumfir.utils.exceptions import MyValidationError

class SignUpController(GenericAPIView): 
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny] 
    
    def post(self, request, *args, **kwargs): 
        validatedData = SignUpSerializer(data = request.data)
        is_valid = validatedData.is_valid()
        if is_valid:
            user = validatedData.save()
            return Response({
                        "message": "Successfully signed up", 
                        "data": {
                            **UserSerializer(user).data, 
                            "token": Token.objects.create(user = user).key
                            }, 
                        "status_code": 201
                        }, 
                    status=201,
                )
        raise MyValidationError(validatedData.errors)