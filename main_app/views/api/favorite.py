from django.http import HttpRequest, HttpResponse, JsonResponse

from ...models import Favorite, Game, User

def add(request: HttpRequest, game_id: int, user_id: int) -> JsonResponse:
    try:
        Favorite.objects.create(user_id=user_id, game_id=game_id)
        return JsonResponse({"success": "true"})
    except Exception as e:
        return JsonResponse({"error": e})

def remove(request: HttpRequest, game_id: int, user_id: int) -> JsonResponse:
    try:
        fav = Favorite.objects.get(user_id=user_id, game_id=game_id)
        if not fav:
            return JsonResponse({"error": "no existing favorite for request"})
        else:
            fav.delete()
            return JsonResponse({"success": "true"})
    except Exception as e:
        return JsonResponse({"error": e})