from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from ..models.helpers import create_or_update_single_screenshot

# deprecated
@login_required
def create(request: HttpRequest, game_id: int) -> HttpResponse:
    """
        Receives a file with input name: "screenshot"
        Replaces or creates a single screenshot for a Game

        Deprecated:
            No longer using this view. We're using helper functions inside
            the game create and update views.
    """
    screenshot_file: UploadedFile = request.FILES.get("screenshot", None)

    if screenshot_file:
        create_or_update_single_screenshot(screenshot_file, game_id)

    return redirect("games_detail", pk=game_id)
