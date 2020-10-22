from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django import forms

from .models import User, Listing, Bids, Watchlist, Comments

# home/main page display active listings
def index(request):
    return render(request, "auctions/index.html", {
        "Listings" : Listing.objects.exclude(active=False),
        "items" : len(Watchlist.objects.filter(user=request.user.username))
    })


# login user function
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# logout user function
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# register new user function
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# List of category items
List_Category = [('None','None'),('ENTERTAINMENT','Entertainment'),('ELECTRONICS', 'Electronics'),('HOME', 'Home'),('HEALTH', 'Health'),('PETS', 'Pets'),('TOYS', 'Toys'),('FASHION', 'Fashion'),('SPORTS', 'Sports'),('BABY', 'Baby'),('TRAVEL', 'Travel')]
# new listing form info
class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder' : 'Title', 'class' : 'form-control', 'autocomplete' : 'off'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Description', 'class' : 'form-control', 'rows' : 8}))
    category = forms.CharField(label='Category', required=False, widget=forms.Select(choices= List_Category, attrs={'class':"mdb-select md-form colorful-select dropdown-primary"}))
    image = forms.CharField(label="Image URL", required=False, widget=forms.TextInput(attrs={'placeholder' : 'Image URL', 'class' : 'form-control', 'autocomplete' : 'off'}))
    price = forms.DecimalField(decimal_places=2, max_digits=12, label="Starting Price")
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
# checking/adding new file
@login_required
def clisting(request):
    if request.method == "POST":
        # get data given
        form = NewListingForm(request.POST)
        # if data is good
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            price = form.cleaned_data["price"]
            # price not high enough
            if price <= 0.001:
                return render(request, "auctions/clisting.html", {
                "form": form,
                "existing": True,
                "message" : "Price should be greater than 0"
            })
            # saving new file
            try:
                listing = Listing(creator=request.user, title=title, description=description, price=price, image=image, category=category)
                listing.save()
                return HttpResponseRedirect(reverse("index"))
            # just in case
            except IntegrityError:
                return render(request, "auctions/clisting.html", {
                "form": form,
                "existing": True,
                "message": "This Listing already exists.",
                "entry": title
                })
        # form not valid so redisplay blank page
        else:
            return render(request, "auctions/clisting.html", {
            "form": form,
            "existing": False
            })
    # method is get so display blank page
    else:
        return render(request, "auctions/clisting.html", {
        "form": NewListingForm(),
        "existing": False
        })


# new comment form
class NewCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Comment', 'class' : 'form-control', 'rows' : 6}))
# render listing page
def slisting(request, id):
    # getting listing data
    try:
        listing = Listing.objects.get(id=id)
    except:
        return HttpResponseRedirect(reverse("index"))
    # check if user is owner for close bid option
    if request.user == listing.creator:
        owner = 'owner'
    else:
        owner = 'not'
    # if user is winner display that he won
    if request.user == listing.winner:
        winner = 'winner'
    else:
        winner = 'not'
    # getting watchlist data to add/remove option
    try:
        temp_w = []
        watch = Watchlist.objects.filter(user=request.user.username)
        for x in watch:
            temp_w.append(x.listing_id)
        if listing.id in temp_w:
            watched = "on list"
        else:
            watched = 'not'
    except:
        watched = "not"
        f"Error in getting info or not found"
    # checking if any comments on listing
    try:
        comments = Comments.objects.filter(listing_id=id)
    except:
        comments = "none"
        "error or none found"
    # checking bids for current price
    try:
        bid_l = Bids.objects.filter(item=listing.title).order_by('price_bid')
        temp = []
        for x in bid_l: 
            temp.append(x.price_bid)
        bid = max(temp)
        return render(request, "auctions/slisting.html",{
        "listing" : listing,
        "bid" : bid,
        "watched" : watched,
        "owner" : owner,
        "winner" : winner,
        "form": NewCommentForm(),
        "comments" : comments,
        "items" : len(Watchlist.objects.filter(user=request.user.username))
    })
    except:
        f"Error in getting info or not found"
    # return data if no bids found
    return render(request, "auctions/slisting.html",{
        "listing" : listing,
        "watched" : watched,
        "owner" : owner,
        "winner" : winner,
        "form": NewCommentForm(),
        "comments" : comments,
        "items" : len(Watchlist.objects.filter(user=request.user.username))
    })


# check and place bid
@login_required
def bid(request, id):
    # getting data of bid, bids, current price
    if request.method == "POST":
        listing = Listing.objects.get(id=id)
        price = listing.price
        bid_amount = request.POST["bid"]
        # checking there was input
        if len(bid_amount) == 0:
            messages.info(request, "Bid must have a value.")
            return redirect('SeeListing', id=id)
        # setting bid value in case first bid
        bid = 0
        # getting current highest bid if any
        try:
            bid_l = Bids.objects.filter(item=listing.title).order_by('price_bid')
            temp = []
            for x in bid_l: 
                temp.append(x.price_bid)
            bid = max(temp)
        except:
            f"Error in getting info or not found"
        # checking new bid is higher than current price
        if price < float(bid_amount) and float(bid_amount) > bid:
            # saving new bid and redirecting with message
            try:
                bid = Bids(creator=request.user, price_bid=bid_amount, item=listing.title)
                bid.save()
                messages.info(request, f"Bid successful! Your Input: {bid_amount}")
                return redirect('SeeListing', id=id)
            # just in case
            except:
                return HttpResponseRedirect(reverse("index"))
        # bid not high enough redirect and display message
        else:
            messages.warning(request, f"Bid must be higher than current bid price. Your Input: {bid_amount}")
            return redirect('SeeListing', id=id)


# adding item to wathlist db by id of listing
@login_required
def watchlist(request, id):
    # if post add to watchlist db
    if request.method == "POST":
        # if logged in
        if request.user.username:
            listing = Listing.objects.get(id=id)
            w = Watchlist(user=request.user.username, listing=listing.title, listing_id=id)
            w.save()
            messages.info(request, f"Added to Watchlist!")
            return redirect('SeeListing', id=id)
        # else just in case
        else:
            return HttpResponseRedirect(reverse("index"))
    # else just in case
    else:
        return HttpResponseRedirect(reverse("index"))


# removing item from watchlist db
@login_required
def remove_watchlist(request, id):
    # if post remove item from db that matches user
    if request.method == "POST":
        if request.user.username:
            Watchlist.objects.filter(Q(listing_id=id),Q(user=request.user.username)).delete()
            messages.info(request, f"Removed from Watchlist!")
            return redirect('SeeListing', id=id)
        else:
            return HttpResponseRedirect(reverse("index"))
    # else just in case
    else:
        return HttpResponseRedirect(reverse("index"))


# rendering watchlist page
def watched(request):
    # get active listings from db
    try:
        items = Watchlist.objects.filter(user=request.user.username)
        temp = []
        for x in items:
            temp.append(x.listing_id)
        listings = []
        for y in temp:
            try:
                listing = Listing.objects.get(Q(id=y),Q(active=True))
            except:
                "listing not active"
        listings.append(listing)
        return render(request, "auctions/watchlist.html", {
            "Listings" : listings
        })
    # if no items on watchlist
    except:
        return render(request, "auctions/watchlist.html", {
            'message' : "No items on watch list."
        })



# comment function
@login_required
def comment(request, id):
    if request.method == "POST":
        # getting form data
        form = NewCommentForm(request.POST)
        # if data is good
        if form.is_valid():
            text = form.cleaned_data["text"]
        c = Comments(user=request.user.username, text=text, listing_id=id)
        c.save()
        messages.info(request, f"Comment added.")
        return redirect('SeeListing', id=id)
    # else just in case
    else:
        return HttpResponseRedirect(reverse("index"))


# category function
def category(request):
    # repeated list of categories (should restructure)
    categories = ['None','Entertainment','Electronics','Home','Health','Pets','Toys','Fashion','Sports','Baby','Travel']
    # if post then display listing if any
    if request.method == "POST":
        category = request.POST["category"]
        return render(request, "auctions/category.html", {
            "Listings" : Listing.objects.filter(Q(category=category.upper()),Q(active=True)),
            "categories" : categories
        })
    # else select menu
    else:
        return render(request, "auctions/category.html", {
            "categories" : categories
        })


# close bid function
@login_required
def closeBid(request, id):
    # should find a way to merge db's
    listing = Listing.objects.get(id=id)
    bid_l = Bids.objects.filter(item=listing.title).order_by('price_bid')
    temp = []
    for x in bid_l: 
        temp.append(x.price_bid)
    bid = max(temp)
    win_bid = Bids.objects.get(Q(item=listing.title),Q(price_bid=bid))
    winner = User.objects.get(username=win_bid.creator)
    Listing.objects.filter(id=id).update(active=False, winner=winner)
    Watchlist.objects.filter(listing_id=id).delete()
    return redirect('SeeListing', id=id)