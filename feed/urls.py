
from django.contrib import admin
from django.urls import path
from feed.controllers.category import CategoryController
from feed.controllers.category_feed import CategoryFeedController
from feed.controllers.dislike_action import DislikeActionController

from feed.controllers.explore import ExploreController
from feed.controllers.feed import FeedController
from feed.controllers.like_action import LikeActionController
from feed.controllers.search import SearchController
from feed.controllers.similar_post import SimilarPostController
from feed.controllers.trending import TrendingController

# WHAT APIS DO YOU NEED
# get - > feed/recommended/ -> List<Post>
# get - > feed/recommended/:id -> Post
# post - > feed/recommended/ 
# delete - > feed/recommended/:id 
# put - > feed/recommended/:id 


post_url_patterns = [
    path('post/<int:post_id>/like', LikeActionController.as_view()),
    path('post/<int:post_id>/dislike', DislikeActionController.as_view()),
    path('post/similar/<int:post_id>', SimilarPostController.as_view(),),
]

feed_url_patterns = [
    path('landing/trending/<int:page>', TrendingController.as_view(),),
    path('landing/explore/<int:page>/session/<str:session_id>', ExploreController.as_view(),),
    path('landing/<int:page>/session/<str:session_id>', FeedController.as_view(),),
    path('landing/<int:page>/<str:search>', SearchController.as_view()),
]

category_url_patterns = [
    path('category', CategoryController.as_view()),
    path('category/<int:category_id>', CategoryFeedController.as_view(),),
]

urlpatterns = post_url_patterns + feed_url_patterns + category_url_patterns
