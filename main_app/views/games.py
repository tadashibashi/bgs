from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from main_app.forms import GameCreateForm
from main_app.models import Game
from main_app.models.helpers import create_screenshot, create_or_update_single_screenshot
import requests

def index(request: HttpRequest):
    """
        Displays the games listing page
        Routing: "games/"
        Name: "games_index"
    """
    q = request.GET.get("q", None)
    games = None
    if q:
        try:
            print(q)
            game_ids = requests.get(request.scheme + "://" + request.get_host() + reverse("search_games") + "?q=" + q)
            game_ids = game_ids.json()
            game_ids = game_ids["games"]
            print(game_ids)
            games = Game.objects.filter(id__in=game_ids)
        except Exception as e:
            print("Error while searching for games in games index", e)
            redirect("games_index")

        query_title = "Results for: " + q
    else:
        games = Game.objects.all().order_by("-created_at")
        query_title = "Latest Games"
    return render(request, "games/index.html", {
        "games": games,
        "query_title": query_title
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
            new_game: Game = form.save(commit=False)
            new_game.user_id = user.id

            # once user_id set, the Tags will be associable
            # form.save sets the tags
            new_game.save()

            if request.FILES.get("screenshot"):
                screenshot = create_screenshot(request.FILES.get("screenshot"), new_game.id)
                new_game.screenshot_set.add(screenshot)
                new_game.save()


            return redirect("games_detail", pk=new_game.id)
        else:
            return render(request, "games/form.html", {
                "form": form,
                "errors": form.errors,
            })



def detail(request: HttpRequest, pk: int) -> HttpResponse:
    game = get_object_or_404(Game, id=pk)

    # inc times_viewed when any user except the creator views
    if request.user.id != game.user_id:
        # set times_viewed, using F to prevent potential race condition
        game.times_viewed = F("times_viewed") + 1
        game.save()

        # get the object again to read from db
        game = Game.objects.get(id=pk)

    # can review?
    if request.user.is_authenticated:
        if request.user.id == game.user_id:
            can_review = False
        else:
            if request.user.review_set.filter(game=game).count():
                can_review = False
            else:
                can_review = True
    else:
        can_review = False

    return render(request, "games/detail.html",
                  {"game": game, "can_review": can_review})



@login_required
def update(request: HttpRequest, pk: int) -> HttpResponse:
    """
        Handles both GET & POST methods.
        GET: Displays the Game edit form
        POST: Submits Game edits made on the form
    """
    game = get_object_or_404(Game, id=pk)
    if request.method == "GET":
        form = GameCreateForm(instance=game)
        return render(request, "games/form.html",
                      {"game": game, "form": form})
    elif request.method == "POST":
        form = GameCreateForm(request.POST, instance=game)
        if form.is_valid():
            if request.FILES.get("screenshot"):
                if not create_or_update_single_screenshot(request.FILES.get("screenshot"), game.id):
                    print("error while creating or updating Game's screenshot")
            form.save()

    return redirect( "games_detail",pk=game.id)



@login_required
def delete(request: HttpRequest, pk: int) -> HttpResponse:
    game = get_object_or_404(Game, pk=pk)
    if request.method == "POST":
        game.delete()

    return redirect("games_index")
