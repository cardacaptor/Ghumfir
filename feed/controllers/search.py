from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.permissions import * 
from rest_framework.generics import *
from django.contrib.auth.decorators import *
from feed.models.post import Post
from feed.model_serializers.post_serializer import PostSerializer
from ghumfir.serializers.pagination_serializer import PaginationWithSearch
from ghumfir.utils.exceptions import MyValidationError
from ..serializers import *
from django.contrib.auth import *
from ..models import *
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

class SearchController(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        pagination  = PaginationWithSearch(data = kwargs)
        isValid = pagination.is_valid()
        if isValid:
            size = 3
            search_text = str(pagination.data["search"]).strip()
            start = (pagination.data["page"] - 1) * size
            end = start + size
            posts = Post.objects.filter(caption__contains = search_text)
            paginated_posts = PostSerializer(posts[start+1:end+1], many = True).data
            return Response({
                            "data": paginated_posts, 
                            "status_code": 201,
                            "message": "Results for '{}' successfully loaded".format(search_text),
                            },
                            status= 200
                            )
        raise MyValidationError(pagination.errors)
