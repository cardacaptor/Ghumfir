
from django.contrib import admin
from django.urls import path
from feed.controllers.dislike_action import DislikeActionView

from feed.controllers.feed import *
from feed.controllers.like_action import LikeActionView
from feed.controllers.search import SearchView

# WHAT APIS DO YOU NEED
# get - > feed/recommended/ -> List<Post>
# get - > feed/recommended/:id -> Post


# post - > feed/recommended/ 
# delete - > feed/recommended/:id 
# post - > feed/recommended/:id

urlpatterns = [
    path('<int:page>', FeedView.as_view(),),
    path('<int:post_id>/like', LikeActionView.as_view()),
    path('<int:post_id>/dislike', DislikeActionView.as_view()),
    path('<int:page>/<str:search>', SearchView.as_view()),
    
]
