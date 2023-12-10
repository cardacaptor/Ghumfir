from django.db import models, transaction
from django.contrib.auth.models import User

from feed.models.post import Post

class ActionChoices(models.TextChoices):
    LIKE = 'LK', ('Like')
    DISLIKE = 'DL', ('Dislike')


class PostActionManagesr(models.Manager):
    def create(self, **obj_data):
        with transaction.atomic():
            self.incrementAction(self.post, obj_data["action"])
            return super().create(**obj_data)
        
    def incrementAction(self, post, action):
        if action == ActionChoices.LIKE :
            post.number_of_likes += 1
        elif action == ActionChoices.DISLIKE :
            post.number_of_dislikes += 1
        post.save()
        
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        with transaction.atomic():
            for i in objs:
                self.incrementAction(i.post, i.action)
            return super().bulk_create(objs, batch_size, ignore_conflicts) 

class PostAction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    action = models.TextField(
        choices= ActionChoices.choices,
    )

    objects = PostActionManager()
    
    def __str__(self):
        return str({
            "user":self.user, 
            "post":self.post.caption,
            "action": str(self.action)
            })
        
