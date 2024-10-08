from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *
from feed.model_serializers.post_serializer import PostSerializer
from feed.models.post import Post
from feed.models.post_action import ActionChoices, PostAction
from feed.model_serializers.post_action_serializer import PostActionSerializer

from ghumfir.utils.exceptions import MyValidationError

from ..serializers import *
from django.contrib.auth import *
from ..models import *

# Create your views here.
class DislikeActionController(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs): 
        action = UserActionSerializer(data = kwargs)
        isValid = action.is_valid()
        if isValid:
          post_id = action.data["post_id"]
          post = Post.objects.get(id = post_id)
          action = PostAction.objects.maybe_create(
            post = post, 
            user = request.user, 
            action = ActionChoices.DISLIKE
          )
          post = Post.objects.get(id = post_id)
          message = "Feed post disliked successfully"
          if action == None:
            message = "Feed post un disliked successfully"
          return Response({ 
                        "data": PostSerializer(post).data,  
                        "status_code": 201,
                        "message": message
                        },
                        status= 201
                        )
        raise MyValidationError(action.errors)