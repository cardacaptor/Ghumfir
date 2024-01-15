from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *

from ghumfir.utils.exceptions import MyValidationError
import recommendation

from ..serializers import *
from django.contrib.auth import *
from ..models import *

from ghumfir.wsgi import recommendation

#pagination methodologies
#cursor based
#offset based


# Create your views here.
class FeedView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Pagination
    
    def post(self, request, *args, **kwargs):
        pagination  = Pagination(data = request.data)
        isValid = pagination.is_valid()
        if isValid:
            start = (pagination.data["page"] - 1) * pagination.data["size"]
            end = start + pagination.data["size"]
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
