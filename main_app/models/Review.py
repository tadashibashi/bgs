from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import datetime
from django.utils import timezone

from .Game import Game


class Review(models.Model):
    """
        A review for a game written by a user. Includes text and optional rating.
        Limit one review per user per game.
    """

    # ===== fields ============================================================

    rating = models.IntegerField(default=0, blank=True)
    """
        Rating 1-10, where 1 is terrible, and 10 is great. 0 for no rating. 
        Icebox: use a five star system, using half-star increments
    """


    content = models.TextField(default="", blank=False)
    """
        The text body of the review
    """


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """
        Author of the reivew
    """


    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    """
        Game this review is for
    """


    created_on = models.DateTimeField(default=timezone.now)
    """
        Review created date
    """


    updated_on = models.DateTimeField(default=None, blank=True, null=True)
    """
        Review updated date. If these don't match, put an edit symbol on review.
    """


    # ===== functions =========================================================


    def save(self):
        # auto-set updated_at
        self.updated_on = timezone.now()


        return super().save()


    def __repr__(self) -> str:
        return f"for {self.game.title} by {self.user.username}"


    def __str__(self) -> str:
        return self.__repr__()

