from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from .File import File


class Profile(models.Model):
    """
        Represents the User's main public profile to display their games,
        social links, bio, profile picture, etc.
    """

    # ===== fields ============================================================


    avatar = models.OneToOneField(File, on_delete=models.DO_NOTHING, null=True, blank=True)
    """
        User's profile picture -- displayed in reviews, profile page, etc.

        on_delete set to nothing because we would rather have the behavior
        delete the avatar when the profile is deleted.
    """


    bio = models.TextField(default="")
    """
        Short bio text that appears next to avatar
    """


    social_links = ArrayField(models.URLField(), default=list, null=True, blank=True)
    """
        An array of links to the user's social accounts

        (ArrayField is a special extension of postgreSQL)
    """


    display_name = models.CharField(max_length=100, default="")
    """
        User's display name
    """


    is_dark_mode = models.BooleanField(default= False)
    """
        This is the modelfield for the dark mode
        Its default is false
    
    """


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """
        The profile's associated user

        Profile will auto-delete when User account is deleted
    """


    # ===== functions =========================================================


    def __repr__(self) -> str:
        return f"for {self.user.username}"

    def __str__(self) -> str:
        return self.__repr__()
