from django.db import models

#what happens to old data when you migrate?

# Create your models here.
class Abc(models.Model):
    email = models.EmailField()
    email1 = models.EmailField()