from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("NewList", views.newlist, name="NewList"),
    path("mylist/<int:id>", views.mylist, name="title"),
    path("additem/<int:id>", views.additem, name="additem"),
    path("remitem/<int:id>", views.remitem, name="remitem"),
    path("active/<int:id>", views.active, name="active"),
    path("dellist/<int:id>", views.dellist, name="dellist"),
    path("addPost/", views.addPost, name="addPost")
]