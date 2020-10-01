from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("wiki/<str:edit>/edit", views.edit, name="edit"),
    path("random_my", views.random_my, name="random_my")
]
