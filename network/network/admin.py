from django.contrib import admin

from .models import User, NewPost, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(NewPost)
admin.site.register(Follow)
