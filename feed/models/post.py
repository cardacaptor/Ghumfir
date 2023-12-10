from django.db import models

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
    