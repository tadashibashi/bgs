"""
    URL routing for the main_app
    main_app / urls.py
"""
from functools import partial

from django.urls import path
from . import views

urlpatterns: list[partial] = [
    path("", views.index.home, name="home"),
    path("games/", views.games.index, name="games_index"),
    path("games/create/", views.games.create, name="games_create"),
    path("games/<int:pk>/", views.games.detail, name="games_detail"), # TODO: refactor to games/<str:username>/<str:game_title>/

]
