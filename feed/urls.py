
from django.contrib import admin
from django.urls import path
from feed.controllers.dislike_action import DislikeActionController

from feed.controllers.feed import FeedController
from feed.controllers.like_action import LikeActionController
from feed.controllers.search import SearchController

# WHAT APIS DO YOU NEED
# get - > feed/recommended/ -> List<Post>
# get - > feed/recommended/:id -> Post

 
# post - > feed/recommended/ 
# delete - > feed/recommended/:id 
# post - > feed/recommended/:id

urlpatterns = [
    path('<int:page>', FeedController.as_view(),),
    path('<int:post_id>/like', LikeActionController.as_view()),
    path('<int:post_id>/dislike', DislikeActionController.as_view()),
    path('<int:page>/<str:search>', SearchController.as_view()),
    
]
