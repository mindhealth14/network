from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractUser):
    pass


class Post(models.Model):
    text = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    
     # kEEP TRACK OR COUNT LIKES
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.text
    
    
    

    
    
    
  
    
    




