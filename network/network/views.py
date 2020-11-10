from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse
from django import forms

from .models import User, NewPost, Follow


# form for post, image just a thought
class NewPostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Post', 'class' : 'form-control', 'rows' : 4}))
    #image = forms.CharField(label="Image URL", required=False, widget=forms.TextInput(attrs={'placeholder' : 'Image URL', 'class' : 'form-control', 'autocomplete' : 'off'}))


# render index: all posts, with new post form
def index(request):
    form = NewPostForm(request.POST)
    posts = NewPost.objects.all()
    return render(request, "network/index.html", {
        "posts" : posts.order_by("-timeStamp").all(),
        "form": form
    })


# render following
def following(request):
    flw = Follow.objects.filter(following=request.user)
    # if not following anyone
    if not flw:
        return render(request, "network/following.html", {
        "message" : "Not Following anyone yet!"
        })
    # empty list and getting data
    names = []
    posts = NewPost.objects.order_by("-timeStamp").all()
    # list of following
    for p in posts:
        for f in flw:
            if f.profile.username == p.creator:
                names.append(p)
    # pass list of posts
    return render(request, "network/following.html", {
        "posts" : names
    })


# login
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

# logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# adding new post 
@login_required
def newpost(request):
    if request.method == "POST":
        # get data given
        form = NewPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            #image = form.cleaned_data["image"]
            # add post to db
            try:
                newp = NewPost(creator=request.user.username, text=text, like=0)
                newp.save()
                return HttpResponseRedirect(reverse("index"))
            # just in case
            except IntegrityError:
                return render(request, "network/index.html", {
                "form": form
                })
        # form not valid so redisplay blank page
        else:
            return render(request, "network/index.html", {
            "form": form
            })
    # method is get
    else:
        return render(request, "network/index.html", {
        "form": NewPostForm()
        })


# profile page
def profile(request, name):
    # get data
    try:
        profile = User.objects.get(username=name)
        message = []
        # if logged in
        if request.user.username:
            # check if user follows this profile
            try:
                flw = Follow.objects.filter(profile=profile, following=request.user)
                f = 'yes'
                if not flw:
                    f = ''
            except:
                f = '' 
        # not logged in 
        else:
            f = ''
        # get data to display, posts/following/followers      
        try:
            posts = NewPost.objects.filter(creator=profile)
            flw = Follow.objects.filter(profile=profile)
            followers = len(flw)
            flw = Follow.objects.filter(following=profile)
            following = len(flw)
        # no data
        except:
            "not found"
        # render page with data
        return render(request, "network/profile.html", {
            "posts" : posts,
            "name" : name,
            "follow" : f,
            "following" : following,
            "followers" : followers
        })
    # no profile fo rthis user
    except:
        message.append(f"{name}, not found!")
        return render(request, "network/profile.html", {
            "messages" : message,
            "name" : name
        })


# follow this profile
@login_required
def follow(request, name):
    # if post add to watchlist db
    if request.method == "POST":
        # if logged in
        if request.user.username:
            follow = User.objects.get(username=name)
            f = Follow(profile=follow, following=request.user)
            f.save()
            messages.info(request, f"Now Following!")
            return redirect('profile', name=name)
        # else just in case
        else:
            return HttpResponseRedirect(reverse("index"))
    # else just in case
    else:
        return HttpResponseRedirect(reverse("index"))

# unfollow this profile
@login_required
def unfollow(request, name):
    # if post remove item from db that matches user
    if request.method == "POST":
        if request.user.username:
            Follow.objects.filter(Q(profile=User.objects.get(username=name)),Q(following=request.user)).delete()
            messages.info(request, f"Removed from Following!")
            return redirect('profile', name=name)
        else:
            return HttpResponseRedirect(reverse("index"))
    # else just in case
    else:
        return HttpResponseRedirect(reverse("index"))