from django.db import models
from django.contrib.auth.models import User

from feed.models.post import Post

class ViewSession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='session_user')

    def __str__(self):
        return str(self.user.username) + "'s session"
    
class PostViewed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='viewer')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='views')
    session = models.ForeignKey(ViewSession, on_delete=models.CASCADE, related_name='views')
    
    def __str__(self):
        return str(self.user.username) + "'s view"

