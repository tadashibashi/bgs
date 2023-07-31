"""
    View functions
    main_app / views.py
"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


def home(request: HttpRequest):
    """
        Displays main home landing page
        Routing: ""
        Name: "home"
    """
    return render(request, "home.html")

