
from django.contrib import admin
from django.urls import path

# from feed.views.action import *
from feed.views.feed import *

# WHAT APIS DO YOU NEED
# get - > feed/recommended/ -> List<Post>
# get - > feed/recommended/:id -> Post


# post - > feed/recommended/ 
# delete - > feed/recommended/:id 
# post - > feed/recommended/:id

urlpatterns = [
    path('', FeedView.as_view()),
    
    # path('action', LikeActionView.as_view())
]
