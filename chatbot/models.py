from django.db import models
from django.contrib.auth.models import User

from feed.models.post import Post

class ChatMessage(models.Model):
    isBotMessage = models.BooleanField()
    message = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='creator', null = True)
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.message
    
class MessagePost(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='recommended_post')
    
    
    def __str__(self):
        return self.post.caption
    
     