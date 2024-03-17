from django.contrib import admin
from feed.models.category import Category
from feed.models.post import Post, PostTag, Tag
from feed.models.post_action import PostAction
from feed.models.post_viewed import PostViewed
# Register your models here.q

class PostAdmin(admin.ModelAdmin):
    list_display = ("caption", "name", "url", "price", "duration", "category", "number_of_likes", "number_of_dislikes", "number_of_views")

class PostActionAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "action")

class PostViewedAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "session")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("caption", "url", "number_of_destinations")

class TagAdmin(admin.ModelAdmin):
    list_display = ("key",)

class PostTagAdmin(admin.ModelAdmin):
    list_display = ("value", "post", "tag")

admin.site.register(Post, PostAdmin)
admin.site.register(PostAction, PostActionAdmin)
admin.site.register(PostViewed, PostViewedAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PostTag, PostTagAdmin)