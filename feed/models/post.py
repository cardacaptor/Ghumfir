from django.db import models

class Post(models.Model):
    caption = models.TextField(null = True)
    url = models.ImageField(null = True)
    price = models.FloatField(null = True)
    duration = models.IntegerField(null = True)

    number_of_likes = models.IntegerField(default=0)
    number_of_dislikes = models.IntegerField(default=0)
    number_of_views = models.IntegerField(default=0)

    def __str__(self):
        return str({
            "caption":self.caption, 
            "url":self.url, 
            "price":self.price, 
            "duration":self.duration,
            "number_of_likes":self.number_of_likes, 
            "number_of_dislikes":self.number_of_dislikes, 
            "number_of_views":self.number_of_views
            })
        
class Tag(models.Model):
    key = models.TextField()
    
class PostTag(models.Model):
    value = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

