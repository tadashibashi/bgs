"""
    View functions for the Game model
    main_app / views/ games.py

    index - displays games, with search feature - publicly accessible
    create - displays add game form, and handles submissions on post
    update - displays update game form, and handles submissions on post
    delete - deletes a game
"""
from pathlib import PurePath

import botocore.client
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import UploadedFile
from django.db.models import F
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import boto3

from ..forms import GameCreateForm
from ..forms.GameEditForm import GameEditForm
from ..models import Game, File
from ..models.helpers import create_screenshot, create_or_update_single_screenshot
import requests

from ..util.s3 import get_base_url, boto3_client, get_bucket_name
from ..util.zip import BgsZipfile


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

        games = Game.objects.filter(is_published=True).order_by("-times_viewed")
        query_title = "Popular Games"
    return render(request, "games/index.html", {
        "games": games,
        "query_title": query_title,
        "featured_games": featured_games
    })


def _upload_game_file(file, key_base: str):
    """
        Helper file that uploads a file directly opened from a zip.

        Args:
            file: the file to upload
            key_base: the root folder in s3 to upload the file to
    """
    path = PurePath(file.name)
    path = PurePath(*path.parts[1:]) #  since this is a file extracted from a zip,
                                     #  the first part of the filename is discarded

    File.helpers.s3_upload(file, key_base + str(path))


def _process_zip_upload_for_game(zip_upload: UploadedFile, game: Game):
    """
        Uploads zip file to s3.
        If None, do nothing.
        Make sure to save game afterward, since its URL gets updated.

        location of files: base_url + "user/<user_id>/games/<game_id>/files/"
    """

    if not zip_upload:
        return

    # open zip
    zip_file = BgsZipfile(zip_upload)

    # folder key on s3 to upload to
    folder = f"user/{game.user_id}/games/{game.id}/"

    # upload each file to folder
    for file in zip_file.files:
        _upload_game_file(file, folder + "files/")

    File.helpers.s3_upload(zip_file.file.fp, folder + "/compressed.zip")

    zip_file.close()

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
            new_game.save()

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
                        new_game.save()

            except Exception as e:
                print(f"failed to upload screenshot file for game: {new_game.title}", e)

            zip_upload = request.FILES.get("zip_upload", None)
            if zip_upload:
                _process_zip_upload_for_game(zip_upload, new_game)
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

    try:
        game = get_object_or_404(Game, id=pk)
    except Exception as e:
        return render(request, "games/unavailable.html")

    if not game.is_published:
        if game.user_id != request.user.id and not request.user.is_staff:
            return render(request, "games/unavailable.html")


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

        form = GameEditForm(instance=game)

        return render(request, "games/form.html",
                      {"game": game, "form": form})

    elif request.method == "POST":
        # update the game

        #populate form
        form = GameEditForm(request.POST, instance=game)

        if form.is_valid():

            # update game's screenshot if user uploaded one
            screenshot_upload = request.FILES.get("screenshot")
            if screenshot_upload:

                if not create_or_update_single_screenshot(screenshot_upload, game.id):
                    print("error while creating or updating Game's screenshot")


            # update zip file upload if user uploaded one
            _process_zip_upload_for_game(request.FILES.get("zip_upload"), game)

            # done, commit changes
            form.save()

    return redirect( "games_detail", pk=game.id)

def _delete_contents(s3, bucket: str, folder_key: str, delete_folder=True):
    objects = s3.list_objects(Bucket=bucket, Prefix=folder_key)
    for obj in objects["Contents"]:
        s3.delete_object(Bucket=bucket, Key=obj["Key"])

    if delete_folder:
        s3.delete_object(Bucket=bucket, Key=folder_key)

def delete_files(request: HttpRequest, pk: int) -> HttpResponse:
    """
        Delete files for a game, but not the game itself
        JSON api request
        url: games/<int:pk>/files/delete
    """
    try:
        game = get_object_or_404(Game, pk=pk)
        s3 = boto3_client("s3")

        bucket = get_bucket_name()
        key = f"user/{game.user_id}/games/{game.id}/files/"
        _delete_contents(s3, bucket, key)
        return JsonResponse({"success": "deleted"})
    except Exception as e:
        return JsonResponse({"error": e})


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
        s3 = boto3_client("s3")
        bucket = get_bucket_name()
        key = f"user/{game.user_id}/games/{game.id}/"

        _delete_contents(s3, bucket, key)

        game.delete()
    else:
        raise PermissionDenied()

    return redirect("games_index")
