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
import requests
from django.views.decorators.csrf import csrf_exempt
#from fuzzywuzzy import process

from .models import User, My_List, Item


# FORMS

# List of category items
List_Category = [('LIST','List'),('BOOKS', 'Books'),
        ('MOVIES', 'Movies'),('SPORTS', 'Sports')]

# new listing form info
class NewListForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder' : 'Title', 'class' : 'form-control', 'autocomplete' : 'off'}))
    category = forms.CharField(label='Category', widget=forms.Select(choices= List_Category, attrs={'class': 'form-control'}))


class NewItemForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder' : 'Title', 'class' : 'form-control', 'autocomplete' : 'off'}))
    description = forms.CharField(label="Description", required=False, widget=forms.Textarea(attrs={'placeholder' : 'Description', 'class' : 'form-control', 'rows' : 5}))
    link = forms.CharField(label="Link URL", required=False, widget=forms.TextInput(attrs={'placeholder' : 'Link URL', 'class' : 'form-control', 'autocomplete' : 'off'}))
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
        # check for user lists
        try:
            lists = My_List.objects.filter(creator=request.user)
        except:
            lists = ''
        # check if any lists shared
        try:
            share = My_List.objects.filter(share=request.user)
        except:
            share = ''
    # not logged in 
    else:
        lists = ''
        share = ''
    return render(request, "packList/index.html", {
        "form": NewListForm(),
        "existing": False,
        "lists": lists,
        "share": share
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
    # check if any lists shared
    try:
        share = My_List.objects.filter(share=request.user)
    except:
        share = ''
    return render(request, "packList/my_list.html", {
        "form": NewItemForm(),
        "mlist": mlist,
        "items": items,
        "lists": My_List.objects.filter(creator=request.user),
        "share": share
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
            comments = ''
            link = ''
            image = ''
            description = ''
            
            # if item in book category
            if mlist.category == "BOOKS":
                # link to good reads
                link = f'https://www.goodreads.com/book/title?id={title}'
                # getting data from googlebooksAPI
                title = title.title()
                nospacetitle = title.replace(" ",'%20')
                res = urlopen(f'https://www.googleapis.com/books/v1/volumes?q={nospacetitle}')
                data = json.loads(res.read())
                ti = data.get('totalItems')
                if int(ti) > 0:                   
                    h = data.get('items')
                    volumeInfo = h[0].get('volumeInfo')
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

                    title = bookAPI.get("title")
                    multi = f"Authors: {bookAPI.get('authors')}, Rating: {bookAPI.get('rating')}, Category: {bookAPI.get('categories')}, Pages: {bookAPI.get('pages')}."
                    try:
                        item = Item(l_item=mlist,title=title,multi=multi,text=bookAPI.get("description"),link=link,image=bookAPI.get("image"),comments=comments)
                        item.save()
                        messages.info(request, f"{title}, added to list!")
                        return redirect(mylist, id)
                    # just in case
                    except IntegrityError:
                        messages.info(request, f"Oops something went wrong!")
                        return redirect(mylist, id)
            
            # if item in sports category
            elif mlist.category == "SPORTS":
                link = f"https://www.youtube.com/results?q={title}+highlights"
           
            # if item in movies category
            elif mlist.category == "MOVIES":
                link = f"https://www.youtube.com/results?q={title}+trailer"
                try:
                    apiKey = "d3e99fda"
                    params = {'t':f"{title}",'plot': "full"}
                    data_URL = 'http://www.omdbapi.com/?apikey='+apiKey
                    response = requests.get(data_URL,params=params)
                except requests.RequestException:
                    return None
                search = response.json()
                # check if result has matches
                if search["Response"] == "True":
                    # make dict with data
                    movieAPI = {
                        "title" : search["Title"],
                        "year" : search["Released"],
                        "director" : search["Director"],
                        "genre" : search["Genre"],
                        "rating" : search["imdbRating"],
                        "img" : search["Poster"],
                        "plot" : search["Plot"]}
                    # make multi text
                    multi = f"Released: {movieAPI.get('year')}. Director: {movieAPI.get('director')}. Genre: {movieAPI.get('genre')}. Rating (IMDB): {movieAPI.get('rating')}."
                    # save data in db
                    try:
                        item = Item(l_item=mlist,title=movieAPI.get("title"),multi=multi,text=movieAPI.get("plot"),link=link,image=movieAPI.get("img"),comments=comments)
                        item.save()
                        messages.info(request, f"{title}, added to list!")
                        return redirect(mylist, id)
                    # just in case
                    except IntegrityError:
                        messages.info(request, f"Oops something went wrong!")
                        return redirect(mylist, id)
                
                # title as given not in iex database
                else:
                    messages.info(request, f"{title}, not found in database. {title} added to list!")

            # else LIST category
            else:
                # get data and set message
                description = form.cleaned_data["description"]
                image = form.cleaned_data["image"]
                link = form.cleaned_data["link"]
                messages.info(request, f"{title}, added to list!")
            
            # saving new file
            try:
                item = Item(l_item=mlist,title=title,text=description,link=link,image=image,comments=comments)
                item.save()
                return redirect(mylist, id)
           
            # just in case
            except IntegrityError:
                messages.info(request, f"Oops something went wrong!")
                return redirect(mylist, id)



def remitem(request, id):
    item = Item.objects.get(id=id)
    title = item.title
    mlist = My_List.objects.get(id=item.l_item.id)
    Item.objects.get(id=id).delete()
    messages.info(request, f"{title} Removed!")
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



@csrf_exempt
@login_required
def addPost(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        # if data received
        if data.get("id") is not None:
            post_id = data["id"]
        if data.get("txt") is not None:
            text = data["txt"]
        # update and return data to finish js function
        try:
            item = Item.objects.get(id=post_id)
            comment = item.comments
            comment = comment + "<strong>" + request.user.username +"</strong>:<i> " + text + "</i><br>"
            Item.objects.filter(id=post_id).update(comments=comment)
            return JsonResponse({'post_id' : post_id, 'text': comment, "status" : 201})
        # return if error
        except:
            return JsonResponse({'error' : "Post not Found", "status" : 404})
    return JsonResponse({}, status=400)



@login_required
def share(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        # if data received
        if data.get("id") is not None:
            id = data["id"]
        if data.get("name") is not None:
            text = data["name"]
        try:
            ulist = My_List.objects.get(id=id)
            user = User.objects.get(username=text)
            ulist.share.add(user)
            return JsonResponse({'text': f"Shared with {text}", "status" : 201})
        # return if error
        except:
            return JsonResponse({'error' : "user not added", "status" : 404})
    return JsonResponse({}, status=400)

