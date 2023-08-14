from django.http import HttpRequest, HttpResponse, JsonResponse

from ...models import Favorite, Game, User

def add(request: HttpRequest, game_id: int, user_id: int) -> JsonResponse:
    try:
        Favorite.objects.create(user_id=user_id, game_id=game_id)
        return JsonResponse({"success": "true"})
    except Exception as e:
        return JsonResponse({"success": "false", "error": e})

def remove(request: HttpRequest, game_id: int, user_id: int) -> JsonResponse:
    try:
        try:
            fav = Favorite.objects.get(user_id=user_id, game_id=game_id)
        except Favorite.DoesNotExist:
            return JsonResponse({"error": "no existing favorite for request"})
        else:
            fav.delete()
            return JsonResponse({"success": "true"})
    except Exception as e:
        return JsonResponse({"success": "false", "error": e})


def game_favorite_count(request: HttpRequest, game_id: int) -> JsonResponse:
    try:
        favs = Favorite.objects.filter(game_id=game_id)
        return JsonResponse({"count": favs.count()})
    except Exception as e:
        return JsonResponse({"error": e})

def exists(request: HttpRequest, game_id: int, user_id: int) -> JsonResponse:
    try:
        favs = Favorite.objects.filter(game_id=game_id, user_id=user_id)
        return JsonResponse({"exists": "1" if favs.count() else "0"})
    except Exception as e:
        return JsonResponse({"error": e})
