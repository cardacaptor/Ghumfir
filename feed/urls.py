
from django.contrib import admin
from django.urls import path
from feed.views.dislike_action import DislikeActionView

from feed.views.feed import *
from feed.views.like_action import LikeActionView
from feed.views.search import SearchView

# WHAT APIS DO YOU NEED
# get - > feed/recommended/ -> List<Post>
# get - > feed/recommended/:id -> Post


# post - > feed/recommended/ 
# delete - > feed/recommended/:id 
# post - > feed/recommended/:id

urlpatterns = [
    path('', FeedView.as_view()),
    path('action/like', LikeActionView.as_view()),
    path('action/dislike', DislikeActionView.as_view()),
    path('search', SearchView.as_view()),
    
]
