from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    caption = models.TextField()
    address = models.TextField()
    url = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    number_of_likes = models.IntegerField(default=0)
    number_of_dislikes = models.IntegerField(default=0)
    number_of_views = models.IntegerField(default=0)

    def __str__(self):
        return str({
            "caption":self.caption, 
            "url":self.url, 
            "latitude":self.latitude, 
            "longitude":self.longitude
            })
    
class ActionChoices(models.TextChoices):
    LIKE = 'LK', ('Like')
    DISLIKE = 'DL', ('Dislike')

class PostAction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    action = models.TextField(
        choices= ActionChoices.choices,
    )

    def __str__(self):
        return str({
            "user":self.user.name, 
            "post":self.post.caption,
            "action": str(self.action)
            })

class PostViewed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def __str__(self):
        return str({
            "user":self.user.name, 
            "post":self.post.caption
            })

