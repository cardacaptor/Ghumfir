from django.db import models, transaction
from django.contrib.auth.models import User

from feed.models.post import Post

class ActionChoices(models.TextChoices):
    LIKE = 'LK', ('Like')
    DISLIKE = 'DL', ('Dislike')


class PostActionManager(models.Manager):
    def maybe_create(self, **obj_data):
        with transaction.atomic():
            data_post = obj_data["post"]
            data_action = obj_data["action"]
            data_user = obj_data["user"]
            action = PostAction.objects.filter(post = data_post, user = data_user).first()
            if action != None:
                self.incrementAction(data_post, action.action, -1)
                action.delete()
            if action == None or action.action != data_action:
                self.incrementAction(data_post, data_action, 1)
                return self.create(**obj_data)
            return None
        
        
    def create(self, **obj_data):
        return super().create(**obj_data)
        
    def incrementAction(self, post, action, incrementBy):
        if action == ActionChoices.LIKE :
            post.number_of_likes += incrementBy
        elif action == ActionChoices.DISLIKE :
            post.number_of_dislikes += incrementBy
        post.save()
        
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        with transaction.atomic():
            for i in objs:
                self.incrementAction(i.post, i.action)
            return super().bulk_create(objs, batch_size, ignore_conflicts) 

class PostAction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='actor')
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='actions')
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
        
