from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.db.models import Q
import urllib, json
from urllib.request import urlopen
from fuzzywuzzy import process

from .models import User, My_List, Item, Comment


# FORMS

# List of category items
List_Category = [('LIST','List'),('BOOKS', 'Books'),
        ('MOVIES', 'Movies'),('SPORTS', 'Sports')]

# new listing form info
class NewListForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder' : 'Title', 'class' : 'form-control', 'autocomplete' : 'off'}))
    category = forms.CharField(label='Category', widget=forms.Select(choices= List_Category, attrs={'class': 'form-control'}))


class NewItemForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder' : 'Title/Text', 'class' : 'form-control', 'autocomplete' : 'off'}))
    #link = forms.CharField(label="Link URL", required=False, widget=forms.TextInput(attrs={'placeholder' : 'Link URL', 'class' : 'form-control', 'autocomplete' : 'off'}))
    image = forms.CharField(label="Image URL", required=False, widget=forms.TextInput(attrs={'placeholder' : 'Image URL', 'class' : 'form-control', 'autocomplete' : 'off'}))


# VIEWS

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
            return render(request, "packList/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "packList/login.html")



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
            return render(request, "packList/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "packList/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "packList/register.html")



# index
def index(request):
    # if logged in
    if request.user.username:
        # check if user follows this profile
        try:
            lists = My_List.objects.filter(creator=request.user)
        except:
            lists = '' 
    # not logged in 
    else:
        lists = ''
    return render(request, "packList/index.html", {
        "form": NewListForm(),
        "existing": False,
        "lists": lists
    })



# Adding new list
@login_required
def newlist(request):
    if request.method == "POST":
        # get data given
        form = NewListForm(request.POST)
        # if data is good
        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            # saving new file
            try:
                mlist = My_List(creator=request.user,title=title,category=category.upper())
                mlist.save()
                try:
                    thislist = My_List.objects.order_by("-timeStamp").filter(Q(creator=request.user),Q(title=title))
                except:
                    'something went wrong'
                return redirect(mylist, thislist[0].id)
            # just in case
            except IntegrityError:
                return render(request, "packList/index.html", {
                "form": form,
                "existing": True,
                "message": "This List already exists."
                })
        # form not valid so redisplay blank page
        else:
            return render(request, "packList/index.html", {
            "form": form,
            "existing": False
            })

  

# Render mylist requested
@login_required
def mylist(request, id):
    # method is get
    try:
        mlist = My_List.objects.get(id=id)
    except:
        return render(request, "packList/my_list.html", {
                "messages": ["This List was not found."],
                "lists": My_List.objects.filter(creator=request.user)
                })
    try:
        items = Item.objects.filter(l_item=mlist)
    except:
        items = ["no items",]
    return render(request, "packList/my_list.html", {
        "form": NewItemForm(),
        "mlist": mlist,
        "items": items,
        "lists": My_List.objects.filter(creator=request.user)
        })



# Add item to list
def additem(request, id):
    if request.method == "POST":
        mlist = My_List.objects.get(id=id)
        # get data given
        form = NewItemForm(request.POST)
        # if data is good
        if form.is_valid():
            title = form.cleaned_data["title"]
            link = ''
            image = ''
            
            # if item in book category
            if mlist.category == "BOOKS":
                # link to good reads
                link = f'https://www.goodreads.com/book/title?id={title}'
                # getting data from googlebooksAPI
                nospacetitle = title.replace(" ",'')
                word_list = title.split()
                res_plus = urlopen(f'https://www.googleapis.com/books/v1/volumes?q={nospacetitle}+intitle:{word_list[-1]}')
                data = json.loads(res_plus.read())
                ti = data.get('totalItems')
                if int(ti) == 0:
                    res = urlopen(f'https://www.googleapis.com/books/v1/volumes?q={nospacetitle}')
                    data = json.loads(res.read())
                    ti = data.get('totalItems')
                if int(ti) > 0:                   
                    h = data.get('items')
                    highest = process.extractOne(title,h)
                    dex = h.index(highest[0])
                    volumeInfo = h[dex].get('volumeInfo')
                    bookAPI = {
                        "title": volumeInfo.get('title'),
                        "authors": volumeInfo.get('authors'),
                        "description": volumeInfo.get('description'),
                        "pages": volumeInfo.get('pageCount'),
                        "categories": volumeInfo.get('categories'),
                        "rating": volumeInfo.get('averageRating'),
                        "image": ''
                    }
                    if 'imageLinks' in volumeInfo:
                        img = volumeInfo.get('imageLinks')
                        bookAPI["image"] = img.get('thumbnail')


                    multi = f"Authors: {bookAPI.get('authors')}, Rating: {bookAPI.get('rating')}, Category: {bookAPI.get('categories')}, Pages: {bookAPI.get('pages')}."
                    try:
                        item = Item(l_item=mlist,title=bookAPI.get("title"),multi=multi,text=bookAPI.get("description"),link=link,image=bookAPI.get("image"))
                        item.save()
                        return redirect(mylist, id)
                    # just in case
                    except IntegrityError:
                        messages.info(request, f"Oops something went wrong!")
                        return redirect(mylist, mlist.id)
            # if item in sports category
            elif mlist.category == "SPORTS":
                link = f"https://www.youtube.com/results?q={title}+highlights"
           
            #  if item in movies category
            elif mlist.category == "MOVIES":
                link = f"https://www.youtube.com/results?q={title}+trailer"
            
            else:
                image = form.cleaned_data["image"]
            
            
            # saving new file
            try:
                item = Item(l_item=mlist,title=title,link=link,image=image)
                item.save()
                return redirect(mylist, id)
           
            # just in case
            except IntegrityError:
                messages.info(request, f"Oops something went wrong!")
                return redirect(mylist, mlist.id)



def remitem(request, id):
    item = Item.objects.get(id=id)
    mlist = My_List.objects.get(id=item.l_item.id)
    Item.objects.get(id=id).delete()
    messages.info(request, f"Item Removed!")
    return redirect(mylist, mlist.id)



def active(request, id):
    item = Item.objects.get(id=id)
    mlist = My_List.objects.get(id=item.l_item.id)
    Item.objects.filter(id=id).update(active=False)
    messages.info(request, f"Done!")
    return redirect(mylist, mlist.id)



def dellist(request, id):
    My_List.objects.get(id=id).delete()
    messages.info(request, f"List Removed!")
    return HttpResponseRedirect(reverse("index"))