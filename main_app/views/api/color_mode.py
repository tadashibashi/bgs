from django.http import JsonResponse, HttpRequest, HttpResponse


def get(request: HttpRequest) -> HttpResponse:
    """
        Gets the color mode and sets the browser cookie "color_mode"
        with either "light" or "dark".

        url:   api/color-mode/
        name: "profile_color_mode_get"

        Looks for setting in this order:
         1. user profile setting
         2. pre-existing cookie
         3. default value: "light"
    """

    no_cookie = False
    if request.user.is_authenticated:
        # get from logged in user settings
        prof = request.user.profile
        mode = "dark" if prof.is_dark_mode else "light"
    else:
        # get from existing cookie
        mode = request.COOKIES.get("color_mode")

        # apply default
        if not mode:
            mode = "light"
            no_cookie = True

    res = JsonResponse({"color_mode": mode})
    if no_cookie:
        res.set_cookie("color_mode", mode)
    return res


def set(request: HttpRequest, mode: str) -> HttpResponse:
    """
        Saves the color mode to the current logged-in user's settings.

        url:   api/color-mode/<str:mode>/
        path: "profile_color_mode_set"
    """

    # only authenticated users can set their settings
    if not request.user.is_authenticated:
        return JsonResponse({"error": "user not logged in"})

    # check that the mode is valid
    if mode == "light" or mode == "dark":

        # save setting to user profile
        prof = request.user.profile
        prof.is_dark_mode = mode == "dark"
        prof.save()

        # return result, and set the local cookie
        res = JsonResponse({"color_mode": mode})
        res.set_cookie("color_mode", mode)
        return res
    else:
        return JsonResponse({"error": "invalid mode"})

