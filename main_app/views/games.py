from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from main_app.forms import GameForm
from main_app.models import Game

def index(request: HttpRequest):
    """
        Displays the games listing page
        Routing: "games/"
        Name: "games_index"
    """
    return render(request, "games/index.html")


def create(request: HttpRequest):
    user = request.user
    if request.method == "GET":
        form = GameForm()
        return render(request, "games/form.html",
                      {"form": form})
    elif request.method == "POST":
        print(request.POST)
        form = GameForm(request.POST)
        if form.is_valid():
            # TODO: upload game here


            new_game = form.save(commit=False)
            new_game.user_id = user.id
            new_game.save()
        return redirect("games_index") # TODO: redirect to games_detail with pk=new_game.id

def detail(request: HttpRequest, pk: int):
    game = get_object_or_404(Game, id=pk)
    return render(request, "games/detail.html",
                  {"game": game})

def update(request: HttpRequest, pk: int):
    game = get_object_or_404(Game, id=pk)
    if request.method == "GET":
        form = GameForm()
        return render(request, "games/form.html",
                      {"game": game, "form": form})
    elif request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            form.instance = game
            form.save()
    return redirect(request, "games/detail.html", pk=game.id)
