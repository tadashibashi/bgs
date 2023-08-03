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
    path("games/<int:pk>/update/", views.games.update, name="games_update"),
    path("games/<int:pk>/", views.games.detail, name="games_detail"), # TODO: refactor to games/<str:username>/<str:game_title>/
    path("games/<int:pk>/delete/", views.games.delete, name="games_delete"),
    path("profile/", views.profile.index, name="profile_index"),
    path("profile/<str:username>/", views.profile.profile, name="profile_public"),
    path("profile/update/", views.profile.update, name="profile_update"),
    path('accounts/signup/', views.accounts.signup, name='signup'),
    path("profile/delete/", views.profile.delete, name="profile_delete"),
    path("api/color-mode/<str:mode>/", views.profile.color_mode_set, name="profile_color_mode_set"),
    path("api/color-mode/", views.profile.color_mode_get, name="profile_color_mode_get"),
    path('games/<int:game_id>/add_review/', views.reviews.add_review, name='add_review'),
    path('reviews/<int:review_id>/delete/', views.reviews.delete_review, name='delete_review'),
]
