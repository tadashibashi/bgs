from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from . import File


class Profile(models.Model):
    """
        Represents the User's main public profile to display their games,
        social links, bio, profile picture, etc.
    """

    avatar = models.OneToOneField(File, on_delete=models.CASCADE)
    """user's profile picture fit into a circle -- displayed in all reviews, profile page, etc."""


    bio = models.TextField()
    """short descriptive text that appears next to avatar"""


    social_links = ArrayField(models.URLField())
    """links to the user's social accounts"""


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """associated User model"""
