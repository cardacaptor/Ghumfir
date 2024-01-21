from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from feed.model_serializers.post_serializer import PostSerializer
from feed.models.post import Post

from ..serializers import *
from django.contrib.auth import *
from ..models import *

class CategoryFeedController(GenericAPIView):
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(category_id = kwargs.get("category_id"))
        return Response({
                        "data":  PostSerializer(posts, many = True).data, 
                        "status_code": 200,
                        "message": "Feed for category id {} successfully loaded".format(kwargs.get("category_id")),
                        },
                        status= 200
                        )
