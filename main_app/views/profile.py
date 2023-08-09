from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import ProfileForm
from ..models.helpers import create_file, get_fileext


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
        Serves as a log-in redirect route -> goes to the user's page

        url:   profile/
        name: "profile_index"
    """
    return redirect("profile_public", username=request.user.username)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    """
        Displays a user's public profile, includes editing utilities if owner is logged in.

        url:   profile/<str:username>/
        name: "profile_public"
    """

    target_user = get_object_or_404(User, username=username)
    return render(request, "profile/index.html", {
        "target_user": target_user
    })


@login_required
def update(request: HttpRequest) -> HttpResponse:
    """
        Handles both Profile form display on "GET", and submission on "POST"

        url:  profile/<int:pk>/update/
        name: "profile_update"
    """

    if request.method == "GET":     # display profile update form

        form = ProfileForm()
        return render(request, "profile/form.html", {
            "form": form
        })

    elif request.method == "POST":  # handle profile update form submission

        # populate form
        form = ProfileForm(request.POST, files=request.FILES)

        # check for validity
        is_valid = form.is_valid()

        if is_valid:
            # if password was updated
            if request.POST["password"]:
                # password & confirm_password must match
                is_valid = request.POST["password"] == request.POST["confirm_password"]

        if is_valid:
            user = request.user
            prof = user.profile

            # update user-related fields
            user.username = request.POST["username"]
            user.email = request.POST["email"]

            if request.POST["password"]:
                user.password = request.POST["password"]

            # update profile-related fields
            prof.display_name = request.POST["display_name"]

            avatar_file: UploadedFile = request.FILES.get("avatar", None)

            if avatar_file:

                # create and upload avatar
                avatar = create_file(avatar_file,
                 f"user/{str(user.id)}/profile/avatar{get_fileext(avatar_file)}")

                if avatar:

                    # delete any pre-existing avatar
                    if prof.avatar:
                        prof.avatar.delete()

                    # set the avatar
                    prof.avatar = avatar

                else:
                    # avatar failed to upload/create
                    print("view profile/update error: failed to upload avatar")

            prof.bio = request.POST["bio"]
            prof.social_links = request.POST["social_links"]

            # done, commit changes
            user.save()
            prof.save()

        return redirect("profile_index")


@login_required
def delete(request: HttpRequest, pk: int) -> HttpResponse:
    """
        TODO: implement
    """
    pass


def color_mode_get(request: HttpRequest) -> HttpResponse:
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


def color_mode_set(request: HttpRequest, mode: str) -> HttpResponse:
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

