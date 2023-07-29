"""
    View functions for bgs
    main_app / views.py
"""
from django.shortcuts import render

def home(request):
    """
        Displays main home landing page
        Routing: ""
        Name: "home"
    """
    return render(request, "home.html")
