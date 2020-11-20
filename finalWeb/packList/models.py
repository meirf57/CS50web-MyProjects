from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass


class My_List(models.Model):
    List_Category = [
        ('LIST','List'),
        ('BOOKS', 'Books'),
        ('MOVIES', 'Movies'),
        ('SPORTS', 'Sports')]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=64, verbose_name="title")
    category = models.CharField(choices=List_Category, blank=True, verbose_name="category",null=True, max_length=64)
    share =  models.ManyToManyField(User, blank=True, related_name="share")
    timeStamp = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    # so error doesnt come up vscode
    objects = models.Manager()
    

class Item(models.Model):
    l_item = models.ForeignKey(My_List, on_delete=models.CASCADE, related_name="list_item")
    title = models.CharField(max_length=64, verbose_name="item title")
    multi = models.CharField(max_length=120, verbose_name="multi")
    text = models.CharField(max_length=150, verbose_name="text")
    link = models.URLField(blank=True, verbose_name="link URL", null=True)
    image = models.URLField(blank=True, verbose_name="Image URL", null=True)
    comments = models.CharField(max_length=120, verbose_name="comments")
    active = models.BooleanField(default=True)
    # so error doesnt come up vscode
    objects = models.Manager()