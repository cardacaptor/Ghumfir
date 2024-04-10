from datetime import timedelta, datetime
import random
from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from feed.model_serializers.post_serializer import PostSerializer
from feed.models.post import Post
from feed.models.post_action import PostAction
from feed.models.post_viewed import PostViewed, ViewSession
from ghumfir.serializers.pagination_serializer import PaginationWithSession

from ghumfir.utils.exceptions import MyBadRequest, MyValidationError
import recommendation

from ..serializers import *
from django.contrib.auth import *
from ..models import *

from ghumfir.wsgi import recommendation

#pagination methodologies
#cursor based
#offset based

class TrendingController(GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        pagination  = PaginationWithSession(data = kwargs)
        isValid = pagination.is_valid()
        if isValid:
            page = pagination.data["page"]
            size = 3
            start = (page - 1) * size
            end = start + size
            three_days_ago = datetime.now() - timedelta(days=7)
            subq = "(SELECT post_id FROM feed_postaction WHERE action = 'LK' and created > '{}' GROUP BY post_id ORDER BY Count(*) LIMIT 3)".format(str(three_days_ago))
            trending_posts = Post.objects.raw("SELECT * FROM feed_post where id in {}".format(subq))
            paginated_posts = trending_posts[start:end]
            for i in paginated_posts:
                post = Post.objects.filter(id = i.id).first() 
                post.number_of_views += 1
                post.save()
            return Response({
                            "data": PostSerializer(paginated_posts, many = True).data, 
                            "status_code": 200,
                            "message": "Feed successfully loaded",
                            },
                            status= 200
                            )
        raise MyValidationError(pagination.errors)
