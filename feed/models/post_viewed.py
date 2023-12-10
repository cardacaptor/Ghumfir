from django.db import models
from django.contrib.auth.models import User

from feed.models.post import Post


class PostViewed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def __str__(self):
        return str({
            "user":self.user.name, 
            "post":self.post.caption
            })

