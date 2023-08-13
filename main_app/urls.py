"""
    URL routing for the main_app
    main_app / urls.py
"""
from functools import partial

from django.urls import path
from . import views

urlpatterns: list[partial] = [

    # landing page
    path("", views.index.home, name="home"),

    # games
    path("games/", views.games.index, name="games_index"),
    path("games/create/", views.games.create, name="games_create"),
    path("games/<int:pk>/update/", views.games.update, name="games_update"),
    path("games/<int:pk>/", views.games.detail, name="games_detail"), # TODO: refactor to games/<str:username>/<str:game_title>/
    path("games/<int:pk>/delete/", views.games.delete, name="games_delete"),
    path("games/<int:pk>/delete/files/", views.games.delete_files, name="games_delete_files"),
    # game reviews/comments
    path('games/<int:game_id>/add_review/', views.reviews.add_review, name='add_review'),
    path('reviews/<int:review_id>/edit/', views.reviews.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', views.reviews.delete_review, name='delete_review'),

    # game screenshot
    path('games/<int:game_id>/add_screenshot/', views.screenshots.create, name="screenshots_add"),

    # profile
    path("profile/", views.profile.index, name="profile_index"),
    path("profile/<str:username>/", views.profile.profile, name="profile_public"),
    path("profile/update/", views.profile.update, name="profile_update"),
    path("profile/delete/", views.profile.delete, name="profile_delete"),

    # registration
    path('accounts/signup/', views.accounts.signup, name='signup'),

    # api
    # - color-mode
    path("api/color-mode/<str:mode>/", views.api.color_mode.set, name="profile_color_mode_set"),
    path("api/color-mode/", views.api.color_mode.get, name="profile_color_mode_get"),
    # - search
    path("api/search/games/", views.api.search.search_games, name="search_games"),
    path("api/search/top-tags/", views.api.search.top_tags, name="search_top_tags"),

]
