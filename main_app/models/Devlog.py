import datetime

from django.db import models
from . import Game


class Devlog(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    content = models.TextField(default="")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]
        """last posts appear first"""