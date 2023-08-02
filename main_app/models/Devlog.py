
from django.db import models
from django.utils import timezone

from .Game import Game


class Devlog(models.Model):
    """
        This model represents a public log detailing releases, updates on the
        game's development, bug fixes, personal reflection, etc.
    """

    # ===== fields ============================================================


    date = models.DateTimeField(default=timezone.now)
    """
        date of the post
    """


    content = models.TextField(default="")
    """
        content of the post
    """


    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    """
        game this log is for
        Relationship: Devlog >--- Game
    """


    class Meta:
        ordering = ["-date"]
        """
            sort posts latest date-first, oldest-last 
        """


    def __repr__(self):
        """human-readable string representation"""

        return f"for {self.game.title}, on {self.date}"

    def __str__(self):
        return self.__repr__()