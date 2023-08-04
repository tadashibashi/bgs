from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from ..models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

def signup(request):
    error_message = ""
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user: User = form.save()
            user.profile = Profile(user=user, display_name=user.username)
            user.profile.save()
            user.save()
            login(request, user)
            return redirect("profile_index")
        else: 
            error_message = "Invalid sign up - try again"
    else:
        form = SignupForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)