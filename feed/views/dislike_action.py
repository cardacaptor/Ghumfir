from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *
from feed.models.post_action import ActionChoices, PostAction

from ghumfir.utils.exceptions import MyValidationError

from ..serializers import *
from django.contrib.auth import *
from ..models import *

# Create your views here.
class DislikeActionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostActionSerializer

    def post(self, request, *args, **kwargs): 
        action = PostActionSerializer(data = request.data)
        isValid = action.is_valid()
        if isValid:
          post = Post.objects.get(id = action.data["postId"])
          action = PostAction.objects.maybe_create(
            post = post, 
            user = request.user, 
            action = ActionChoices.DISLIKE
          )
          message = "Feed post disliked successfully"
          if action == None:
            message = "Feed post un disliked successfully"
          return Response({ 
                        "status_code": 201,
                        "message": message
                        },
                        status= 200
                        )
        raise MyValidationError(action.errors)