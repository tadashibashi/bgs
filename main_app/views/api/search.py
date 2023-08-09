from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.text import slugify

from main_app.models import Game, Tag

def top_tags(request: HttpRequest) -> HttpResponse:
    q = request.GET.get("q", "")

    tokens: list[str] = [slugify(token.lower()) for token in q.split(" ")]

    token = tokens[-1]

    tags = [tag["text"] for tag in Tag.objects.filter(text__icontains=token).annotate(count=Count("game")).order_by("-count")[:8].values() if tag["count"] > 0]

    return JsonResponse({"tags": tags})

def search_games(request: HttpRequest) -> HttpResponse:
    params = request.GET
    q = params.get("q", "")

    tokens: list[str] = [slugify(token.lower()) for token in q.split(" ")]

    filtered_tags = Tag.objects.none()
    filtered_games = Game.objects.none()
    filtered_users = User.objects.none()

    for token in tokens:
        filtered_tags |= Tag.objects.filter(text__icontains=token)
        filtered_games |= Game.objects.filter(title__icontains=token)
        filtered_users |= User.objects.filter(username__icontains=token)

    game_ids = {}
    for tag in filtered_tags:
        for game in tag.game_set.all():
            if not game.id in game_ids:
                game_ids[game.id] = 1
            else:
                game_ids[game.id] += 1

    for game in filtered_games:
        if not game.id in game_ids:
            game_ids[game.id] = .5
        else:
            game_ids[game.id] += .5

    for user in filtered_users:
        for game in user.game_set.all():
            if not game.id in game_ids:
                game_ids[game.id] = .15
            else:
                game_ids[game.id] += .15

    game_ids = [key for key, value in sorted(game_ids.items(), key=lambda k: k[1], reverse=True)]

    return JsonResponse({"games": game_ids})