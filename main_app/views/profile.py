"""
    View functions for Profile model
    main_app / views / profile.py

    index - redirects to the logged-in user's profile

    profile - displays user profile

    update - handles both display of update form (GET),
        and update form handling (POST)

    delete - deletes profile
"""
from pathlib import PurePath

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import ProfileForm
from ..models import File


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
                avatar = File.helpers.create_and_upload(avatar_file,
                 f"user/{str(user.id)}/profile/avatar{PurePath(avatar_file.name).suffix}")

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
