from django.contrib import admin
from feed.models.category import Category
from feed.models.post import Post, PostTag, Tag
from feed.models.post_action import PostAction
from feed.models.post_viewed import PostViewed
# Register your models here.q


admin.site.register(Post)
admin.site.register(PostAction)
admin.site.register(PostViewed)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostTag)