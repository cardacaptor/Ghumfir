from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from feed.model_serializers.post_serializer import PostSerializer
from feed.models.post import Post
from ghumfir.serializers.pagination_serializer import Pagination

from ghumfir.utils.exceptions import MyValidationError
import recommendation

from ..serializers import *
from django.contrib.auth import *
from ..models import *

from ghumfir.wsgi import recommendation

class SimilarPostController(GenericAPIView):
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        posts =  recommendation.vectorizerService.sort_rest(kwargs.get("post_id"))
        return Response({
                        "data":  PostSerializer(posts, many = True).data, 
                        "status_code": 200,
                        "message": "Similar posts for post id {} successfully loaded".format(kwargs.get("post_id")),
                        },
                        status= 200
                        )
