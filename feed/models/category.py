from django.db import models

class Category(models.Model):
    caption = models.TextField(null = True)
    url = models.ImageField(null = True)
    number_of_destinations = models.IntegerField(default=0)

    def __str__(self):
        return str(self.caption)