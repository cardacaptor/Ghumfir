from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *
from ghumfir.utils.exceptions import MyValidationError
from ..serializers import *
from django.contrib.auth import *
from ..models import *

# Create your views here.
class SearchView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaginationWithSearch
    
    def post(self, request, *args, **kwargs):
        pagination  = PaginationWithSearch(data = request.data)
        isValid = pagination.is_valid()
        if isValid:
            search_text = str(pagination.data["size"]).strip()
            start = (pagination.data["page"] - 1) * pagination.data["size"]
            end = start + pagination.data["size"]
            posts =  Post.objects.filter()
            paginated_posts = PostSerializer(posts[start+1:end+1], many = True).data
            return Response({
                            "data": paginated_posts, 
                            "status_code": 201,
                            "message": "Results for '{}' successfully loaded".format(search_text),
                            },
                            status= 200
                            )
        raise MyValidationError(pagination.errors)
