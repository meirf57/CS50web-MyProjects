from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing

# home/main page
def index(request):
    return render(request, "auctions/index.html", {
        "Listings" : Listing.objects.all()
    })


List_Category = [('None','none'),('ENTERTAINMENT','Entertainment'),('ELECTRONICS', 'Electronics'),('HOME', 'Home'),('HEALTH', 'Health'),('PETS', 'Pets'),('TOYS', 'Toys'),('FASHION', 'Fashion'),('SPORTS', 'Sports'),('BABY', 'Baby'),('TRAVEL', 'Travel')]
# form info
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
            # saving new file
            try:
                listing = Listing(creator=request.user, title=title, description=description, price=price, image=image, category=category)
                listing.save()
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError:
                return render(request, "auctions/clisting.html", {
                "form": form,
                "existing": True,
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
