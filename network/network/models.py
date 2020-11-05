from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class NewPost(models.Model):
    creator = models.CharField(max_length=64)
    text = models.TextField(verbose_name="Description")
    image = models.URLField(blank=True, verbose_name="Image URL", null=True)
    like = models.IntegerField()
    timeStamp = models.DateTimeField(auto_now_add=True,null=True)
    # for objects error vscode
    objects = models.Manager()
