from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.clisting, name="CreateListing"),
    path("Listing/<int:id>", views.slisting, name="SeeListing"),
    path("Bid/<int:id>", views.bid, name="bid")
]
