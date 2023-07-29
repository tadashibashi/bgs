"""
    View functions
    main_app / views.py
"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def home(request: HttpRequest):
    """
        Displays main home landing page
        Routing: ""
        Name: "home"
    """
    return render(request, "home.html")

def games_index(request: HttpRequest):
    """
        Displays the games listing page
        Routing: "games/"
        Name: "games_index"
    """
    return render(request, "games/index.html")