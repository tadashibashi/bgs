from django.contrib.auth.models import User
from django.db import models

class Favorite(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
