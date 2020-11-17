from django.contrib import admin

# Register your models here.
from .models import User, My_List, Item, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(My_List)
admin.site.register(Item)
admin.site.register(Comment)