from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from main_app.forms import GameCreateForm
from main_app.models import Game



def index(request: HttpRequest):
    """
        Displays the games listing page
        Routing: "games/"
        Name: "games_index"
    """
    games = Game.objects.all().order_by("-created_at")
    return render(request, "games/index.html", {
        "games": games,
    })



@login_required
def create(request: HttpRequest):
    user = request.user
    if request.method == "GET":
        form = GameCreateForm()
        return render(request, "games/form.html",
                      {"form": form})
    elif request.method == "POST":
        form = GameCreateForm(request.POST, files=request.FILES)

        if form.is_valid():
            # TODO: upload game files to AWS S3

            # user and tags not saved yet -- wait to commit
            new_game = form.save(commit=False)
            new_game.user_id = user.id

            # once user_id set, the Tags will be associable
            # form.save sets the tags
            form.save(commit=True)
            return redirect("games_detail", pk=new_game.id)
        else:
            return render(request, "games/form.html", {
                "form": form,
                "errors": form.errors,
            })



def detail(request: HttpRequest, pk: int) -> HttpResponse:
    game = get_object_or_404(Game, id=pk)
    return render(request, "games/detail.html",
                  {"game": game})



@login_required
def update(request: HttpRequest, pk: int) -> HttpResponse:
    game = get_object_or_404(Game, id=pk)
    if request.method == "GET":
        form = GameCreateForm(instance=game)

        return render(request, "games/form.html",
                      {"game": game, "form": form})
    elif request.method == "POST":
        form = GameCreateForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
    return redirect( "games_detail",pk=game.id)



@login_required
def delete(request: HttpRequest, pk: int) -> HttpResponse:
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        game.delete()

        return redirect("games_index")
    else:
        return render(request, "games/delete.html", {
            "game": game,
        })
