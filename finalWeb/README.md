# Final Project for CS50web

## About the website

This is my final project for [Harvard CS50 web](https://cs50.harvard.edu/web/2020/) course. It's a website named *“Pack List”* or *“UList”* that was created as a web application for lists (making and sharing).

The idea came about since at the time I was packing and going places for the weekends. Then it evolved to making lists of different media, to keep or share. Depending on the category of the list, the items on the list are added.  
- Regular: Everything is added manually by the user  
- Books: The title given returns the first item from google books API  
- Movies: The title given returns from omdb API  
- Sports: Returns a link to youtube search of highlights  

The idea is to keep track (and mark done), or share with other users the lists created.

## Description

Web application is based on Django framework.  
I used SQLite3 as database.

## Justification

This project is distinct from all previous projects so far. Why?

- More models with complex relation between them.
- Uses ajax functionality, fetch data without reloading the page.
- Request and load from API.
- Selects and saves data from API request.
- Completely Mobile responsive.

## How to use

To run the web application use these commands:

```
$ python manage.py makemigrations packList
$ python manage.py migrate   
$ python manage.py runserver
```

## Requirements

- install python 3
- install django
- install urllib
- install urllib.request
- install requests