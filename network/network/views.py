from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, NewPost



class NewPostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder' : 'Post', 'class' : 'form-control', 'rows' : 4}))
    #image = forms.CharField(label="Image URL", required=False, widget=forms.TextInput(attrs={'placeholder' : 'Image URL', 'class' : 'form-control', 'autocomplete' : 'off'}))

def index(request):
    form = NewPostForm(request.POST)
    return render(request, "network/index.html", {
        "posts" : NewPost.objects.all(),
        "form": form
    })


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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

    
@login_required
def newpost(request):
    if request.method == "POST":
        # get data given
        form = NewPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            #image = form.cleaned_data["image"]
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


@login_required
def profile(request, name):
    try:
        profile = User.objects.get(username=name)
        try:
            posts = NewPost.objects.filter(creator=profile)
        except:
            posts = "not found"
        return render(request, "network/profile.html", {
            "message" : f"{profile}, hello!",
            "posts" : posts
        })
    except:
        return render(request, "network/profile.html", {
            "message" : f"{name}, not found!"
        })