from django.contrib.auth.models import User
from django.db import models

from . import Game


class Review(models.Model):
    """
        Game review by a User for a game. Includes text and optional rating.
        Limit one review per user per game.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    rating = models.IntegerField()
    """Rating 1-10, where 1 is terrible, and 10 is great. 0 for no rating. 
    Icebox: use a five star system, using half-star increments"""

    content = models.TextField()
    """The text body of the review"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """Author of the post"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    """Game this review is for"""
