from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *
from drf_spectacular.utils import extend_schema
from feed.models.post_action import ActionChoices, PostAction

from ghumfir.utils.exceptions import MyValidationError

from ..serializers import *
from django.contrib.auth import *
from rest_framework.authtoken.models import Token
from ..models import *

# Create your views here.
class LikeActionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeActionSerializer

    def post(self, request, *args, **kwargs): 
        action = LikeActionSerializer(data = request.data)
        isValid = action.is_valid()
        if isValid:
          action = PostAction.objects.create(
            post = Post.objects.get(id = action.data["postId"]), 
            user = request.user, 
            action = ActionChoices.LIKE
            )
          action.save()
          return Response({ 
                        "status_code": 201,
                        "message": "Feed post liked successfully"
                        },
                        status= 200
                        )
        raise MyValidationError(action.errors)