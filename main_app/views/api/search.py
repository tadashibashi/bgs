from django.contrib.postgres.search import SearchVector
from django.http import HttpRequest, HttpResponse, JsonResponse

from main_app.models import Game, Tag


def search_games(request: HttpRequest) -> HttpResponse:
    params = request.GET
    q = params.get("q", "")

    tokens: list[str] = q.split(" ")
    tags = Tag.objects.all()
    filtered_tags = Tag.objects.none()
    filtered_games = Game.objects.none()
    for token in tokens:
        filtered_tags |= tags.filter(text__icontains=token)
        filtered_games |= Game.objects.filter(title__icontains=token)

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

    game_ids = [item[0] for item in sorted(game_ids.items(), key=lambda k: k[1], reverse=True)]

    return JsonResponse({"games": game_ids})