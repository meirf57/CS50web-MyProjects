from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    List_Category = [
        ('ENTERTAINMENT','Entertainment'),
        ('ELECTRONICS', 'Electronics'),
        ('HOME', 'Home'),
        ('HEALTH', 'Health'),
        ('PETS', 'Pets'),
        ('TOYS', 'Toys'),
        ('FASHION', 'Fashion'),
        ('SPORTS', 'Sports'),
        ('BABY', 'Baby'),
        ('TRAVEL', 'Travel')]
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name="listings",null=True)
    title = models.CharField(max_length=64, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    category = models.CharField(choices=List_Category, blank=True, verbose_name="Category",null=True, max_length=64)
    image = models.URLField(blank=True, verbose_name="Image URL", null=True)
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=12, verbose_name="Starting Price")
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timeStamp = models.DateTimeField(auto_now_add=True,null=True)
    
    # to display name of item when searched
    def __str__(self):
        return self.title

class Bids(models.Model):
    creator = models.CharField(max_length=64)
    price_bid = models.DecimalField(blank=True, decimal_places=2, max_digits=12, verbose_name="Bid Price")
    timeStamp = models.DateTimeField(auto_now_add=True,null=True)
    item = models.CharField(max_length=64)

class Comments(models.Model):
    pass

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing = models.CharField(max_length=64)