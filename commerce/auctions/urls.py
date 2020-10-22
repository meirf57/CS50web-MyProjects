from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.clisting, name="CreateListing"),
    path("Listing/<int:id>", views.slisting, name="SeeListing"),
    path("Bid/<int:id>", views.bid, name="bid"),
    path("Watchlist", views.watched, name="watched"),
    path("Watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("RemoveWatchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("Comment/<int:id>", views.comment, name="comment"),
    path("Category", views.category, name="category"),
    path("CloseBid/<int:id>", views.closeBid, name="closeBid"),
]
