from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


from ..forms import GameCreateForm
from ..models import Game
from ..models.helpers import create_screenshot, create_or_update_single_screenshot
import requests


def index(request: HttpRequest):
    """
        Displays the games listing page
        Shows games based on a search query if any was provided

        url:  "games/"
        query: q=search+terms+here
        name: "games_index"
    """
    q = request.GET.get("q", None)
    games = None
    featured_games = []
    if q:   # if there is a query
        try:
            # get list of games for query
            game_ids = requests.get(request.scheme + "://" + request.get_host() + reverse("search_games") + "?q=" + q)
            game_ids = game_ids.json()
            game_ids = game_ids["games"]

            games = Game.objects.filter(id__in=game_ids)
        except Exception as e:
            print("Error while searching for games in games index", e)
            redirect("games_index")

        query_title = "Results for: " + q
    else:  # if no query, display featured & latest games
        featured_games.append(Game.objects.filter(user__username="aaron").first())
        featured_games.append(Game.objects.filter(user__username="aaron").last())
        featured_games.append(Game.objects.filter(user__username="user1").first())

        games = Game.objects.all().order_by("-times_viewed")
        query_title = "Popular Games"
    return render(request, "games/index.html", {
        "games": games,
        "query_title": query_title,
        "featured_games": featured_games
    })



@login_required
def create(request: HttpRequest):
    """
        Displays a form to create a new game on GET,
        and submits that form on POST

        url:  /games/create
        name: "games_create"
    """

    if request.method == "GET":
        # show creation form
        form = GameCreateForm()
        return render(request, "games/form.html",
                      {"form": form})

    elif request.method == "POST":
        # create the game

        # populate form
        form = GameCreateForm(request.POST, files=request.FILES)

        if form.is_valid():

            # user, a required field, must be associated to game before saving to postgres
            new_game: Game = form.save(commit=False)
            new_game.user_id = request.user.id



            # upload and set screenshot if user provided one
            screenshot_file = request.FILES.get("screenshot", None)

            try:
                if screenshot_file:
                    # create screenshot from file
                    screenshot = create_screenshot(request.FILES.get("screenshot"), new_game.id)

                    # add it to game if it created
                    if screenshot is None:
                        print(f"failed to upload or create screenshot for game: {new_game.title}")
                    else:
                        new_game.screenshot_set.add(screenshot)

            except Exception as e:
                print(f"failed to upload screenshot file for game: {new_game.title}", e)

            new_game.save()

            return redirect("games_detail", pk=new_game.id)
        else:
            return render(request, "games/form.html", {
                "form": form,
                "errors": form.errors,
            })



def _can_review_game(user: User, game: Game) -> bool:
    """
        Helper function to check whether the current user can review the game
    """

    # staff can review no matter what
    if user.is_staff:
        can_review = True
    else:
        # user must be logged in to review
        if user.is_authenticated:

            # user can review game if they are not its creator
            if user.id == game.user_id:
                can_review = False
            else:
                # user can review a game only once
                if user.review_set.filter(game_id=game.id).count():
                    can_review = False
                else:
                    can_review = True
        else:
            can_review = False
    return can_review


def detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
        Displays a game's unique page. Shows game window, details, comments, etc.

        url:  games/<int:pk/
        name: "games_detail"
    """

    game = get_object_or_404(Game, id=pk)

    # increase times_viewed when any user except the creator views it
    if request.user.id != game.user_id:
        times_viewed = game.times_viewed

        # set views via F to prevent potential errors from race conditions
        game.times_viewed = F("times_viewed") + 1
        game.save()

        # set it temporarily to read in template, don't save
        # (otherwise it appears as F(times_viewed) + 1)
        game.times_viewed = times_viewed + 1

    return render(request, "games/detail.html",
                  {
                      "game": game,
                      "can_review": _can_review_game(request.user, game)
                  })



@login_required
def update(request: HttpRequest, pk: int) -> HttpResponse:
    """
        Handles both GET & POST methods for editing a Game.
        GET: Displays the Game edit form
        POST: Submits Game edits made on the form

        url: games/<int:pk>/update/
        name: games_update
    """

    game = get_object_or_404(Game, id=pk)


    if request.method == "GET":
        # display update form to the user

        form = GameCreateForm(instance=game)

        return render(request, "games/form.html",
                      {"game": game, "form": form})

    elif request.method == "POST":
        # update the game

        #populate form
        form = GameCreateForm(request.POST, instance=game)

        if form.is_valid():

            # update game's screenshot if user uploaded one
            if request.FILES.get("screenshot"):

                if not create_or_update_single_screenshot(request.FILES.get("screenshot"), game.id):
                    print("error while creating or updating Game's screenshot")

            # done, commit changes
            form.save()

    return redirect( "games_detail", pk=game.id)



@login_required
def delete(request: HttpRequest, pk: int) -> HttpResponse:
    """
        Delete a game

        url:   games/<int:pk>/delete/
        name: "games_delete"
    """

    game = get_object_or_404(Game, pk=pk)

    # only staff and game creator can delete game
    if request.user.is_staff or request.user.id == game.user_id:
        game.delete()
    else:
        raise PermissionDenied()

    return redirect("games_index")
