from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from ..forms import ProfileForm


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """
        Displays user portal, the main profile page + editing utilities
        Route: profile/
        Name: "profile"
    """

    return render(request, "profile/index.html")


@login_required
def update(request: HttpRequest) -> HttpResponse:
    """
        Handles both Profile form display on "GET", and submission on "POST"
        Route: profile/update/
        Name: "profile_update"
    """


    if request.method == "GET":
        form = ProfileForm()
        return render(request, "profile/form.html", {
            "form": form
        })

    elif request.method == "POST":

        form = ProfileForm(request.POST, files=request.FILES)
        is_valid = form.is_valid()
        if is_valid:
            if request.POST["password"]:
                is_valid = request.POST["password"] == request.POST["confirm_password"]

        print(request.POST)

        if is_valid:
            user = request.user
            profile = user.profile

            user.username = request.POST["username"]
            profile.display_name = request.POST["display_name"]
            user.email = request.POST["email"]

            if request.POST["password"]:
                user.password = request.POST["password"]

            # TODO: upload profile image file to S3
            if request.FILES["avatar"]:
                # profile.avatar = request.FILES["avatar"]
                pass

            profile.bio = request.POST["bio"]

            profile.social_links = request.POST["social_links"]

            user.save()
            profile.save()

        return redirect("profile_index")


@login_required
def delete(request: HttpRequest) -> HttpResponse:
    pass