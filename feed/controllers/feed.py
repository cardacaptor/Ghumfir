from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from feed.model_serializers.post_serializer import PostSerializer
from ghumfir.serializers.pagination_serializer import Pagination

from ghumfir.utils.exceptions import MyValidationError
import recommendation

from ..serializers import *
from django.contrib.auth import *
from ..models import *

from ghumfir.wsgi import recommendation

#pagination methodologies
#cursor based
#offset based

class FeedController(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        pagination  = Pagination(data = kwargs)
        isValid = pagination.is_valid()
        if isValid:
            size = 3
            start = (pagination.data["page"] - 1) * size
            end = start + size
            last_activity = recommendation.get_corpus_by_index(request.user)
            posts =  recommendation.sort_rest(request.user)
            paginated_posts = PostSerializer(posts[start+1:end+1], many = True).data
            return Response({
                            "data": paginated_posts, 
                            "status_code": 201,
                            "message": "Feed successfully loaded",
                            **last_activity,
                            },
                            status= 200
                            )
        raise MyValidationError(pagination.errors)
