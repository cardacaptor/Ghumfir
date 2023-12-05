from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *
from drf_spectacular.utils import extend_schema

from .validators.user_validator import *
from .serializers import *
from django.contrib.auth import *
from rest_framework.authtoken.models import Token

class SignUpView(GenericAPIView): 
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
    
class SignInView(GenericAPIView): 
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]

    #{username: 1, password: 2}
    #{username: "sajat"}
    #{password: "sajat"}
    
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
    
class GetMeView(GenericAPIView): 
    def get(self, request, *args, **kwargs): 
        return Response({
                    "message": "Data load successful", 
                    "data": UserSerializer(request.user).data,
                    "status_code": 201
                    }, 
                status=201,
            )

    