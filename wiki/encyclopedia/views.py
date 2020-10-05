from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown import markdown
from django import forms
import random

from . import util


# get list of items in db
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# getting data from db of item
def title(request, title):
    g = util.get_entry(title)
    # if item in entry retrieve data
    if g != None:
        html = markdown(g)
        return render(request, "encyclopedia/title.html", {
        "title" : html,
        "t": title
        })
    # else return apology
    else:
        return render(request, "encyclopedia/apology.html", {
        "sorry" : f"{title.capitalize()}, was not found."
        })


# form info
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class' : 'form-control', 'autocomplete' : 'off'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control', 'rows' : 8}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
# checking/adding new file
def new(request):
    if request.method == "POST":
        # get data given
        form = NewEntryForm(request.POST)
        # if data is good
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            # if doesn't contradict other data in db
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                # saving new file
                util.save_entry(title,text)
                # retrieving and displaying file
                g = util.get_entry(title)
                if g != None:
                    html = markdown(g)
                    return render(request, "encyclopedia/title.html", {
                    "title" : html,
                    "t": title
                    })
            # set page to existing file to display alerts
            else:
                return render(request, "encyclopedia/new.html", {
                "form": form,
                "existing": True,
                "entry": title
                })
        # form not valid so redisplay blank page
        else:
            return render(request, "encyclopedia/new.html", {
            "form": form,
            "existing": False
            })
    # method is get so display blank page
    else:
        return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm(),
        "existing": False
        })


# link to change data in db of existing item
def edit(request, edit):
    text = util.get_entry(edit)
    form = NewEntryForm()
    form.fields["title"].initial = edit
    form.fields["text"].initial = text
    form.fields["edit"].initial = True
    return render(request, "encyclopedia/new.html", {
    "form": form,
    "edit": form.fields["edit"].initial,
    "entry": form.fields["title"].initial
    })



# search for item or similar else return apology
def search(request):
    # value given
    value = request.GET.get('q','')
    #list of values in db
    entry_l = util.list_entries()
    empty_l = []
    # loop to find similarities
    for x in range(len(entry_l)):
        # if in db present info from db
        if value.lower() == entry_l[x].lower():
            g = util.get_entry(value)
            if g != None:
                html = markdown(g)
                return render(request, "encyclopedia/title.html", {
                "title" : html,
                "t": entry_l[x]
                })
        # if value part of str of list in db
        elif value.lower() in entry_l[x].lower():
            empty_l.append(entry_l[x])
    # if similar strings found return list of items found
    if len(empty_l) > 0:
         return render(request, "encyclopedia/search.html", {
            "entries": empty_l,
            "value" : value.capitalize()
            })
    # return apology if not in db
    else:
        return render(request, "encyclopedia/search.html", {
            "value" : f"{value.capitalize()}, was not found."
            })


# selecting random item from list
def random_my(request):
    # temp list to select item from
    temp_l = util.list_entries()
    y = len(temp_l)
    # random number of items in list
    x = random.randint(0,y - 1)
    # getting data of selected item
    title = temp_l[x]
    g = util.get_entry(title)
    # accessing data of item to set page
    if g != None:
        html = markdown(g)
        return render(request, "encyclopedia/title.html", {
        "title" : html,
        "t": temp_l[x]
        })