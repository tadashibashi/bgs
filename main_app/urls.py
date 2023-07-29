"""
    URL routing for the main_app
    main_app / urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("games/", views.games_index, name="games_index")
]
