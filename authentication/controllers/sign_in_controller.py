
from django.contrib.auth import *
from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from authentication.serializers.model_serializer import UserSerializer

from rest_framework.authtoken.models import Token
from authentication.serializers.serializers import SignInSerializer
from ghumfir.utils.exceptions import MyValidationError

class SignInController(GenericAPIView): 
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs): 
        validatedData = SignInSerializer(data = request.data)
        is_valid = validatedData.is_valid()
        if is_valid:
            user = authenticate(**validatedData.data)
            if user is not None:
                return Response({
                            "message": "Successfully signed in", 
                            "data": {
                                **UserSerializer(user).data, 
                                "token": Token.objects.get(user = user).key,
                            },
                            "status_code": 201
                            }, 
                        status=201,
                    )
            raise MyValidationError("Username and Password did not match")
        raise MyValidationError(validatedData.errors)
    