import random
from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.generics import *
from feed.model_serializers.post_serializer import PostSerializer
from feed.models.post import Post
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

class ExploreController(GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        pagination  = PaginationWithSession(data = kwargs)
        isValid = pagination.is_valid()
        if isValid:
            page = pagination.data["page"]
            session_id = pagination.data.get("session_id")
            size = 3
            start = (page - 1) * size
            end = start + size
            if(request.user.id == None):
                posts = list(Post.objects.all())
                random.shuffle(posts)
                paginated_posts = posts[start:end]
                return Response({
                                "session_id":0,
                                "data": PostSerializer(paginated_posts, many = True).data, 
                                "status_code": 200,
                                "message": "Feed successfully loaded",
                                },
                                status= 200
                                )
            if(session_id == 0):
                session = ViewSession.objects.create(user_id = request.user.id)
            else:
                session = ViewSession.objects.get(id = session_id)
            if(session == None):
                raise MyBadRequest("Could not find session")
            allPosts = list(Post.objects.all())
            session_views = PostViewed.objects.filter(session_id = session_id)
            session_views_set = set([i.post_id for i in session_views]) 
            allPosts = [i for i in allPosts if i.id not in session_views_set]
            random.shuffle(allPosts)
            paginated_posts = allPosts[start+1:end+1]
            PostViewed.objects.bulk_create([
                PostViewed(user_id = request.user.id, post_id = i.id, session_id = session.id ) 
                for i in paginated_posts
                ])
            for i in paginated_posts:
                post = Post.objects.filter(id = i.id).first() 
                post.number_of_views += 1
                post.save()
            return Response({
                            "session_id": session.id,
                            "data": PostSerializer(paginated_posts, many = True).data, 
                            "status_code": 200,
                            "message": "Feed successfully loaded",
                            },
                            status= 200
                            )
        raise MyValidationError(pagination.errors)
