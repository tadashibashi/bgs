from django.contrib.auth.models import User
from django.db import models

class Favorite(models.Model):
    game = models.OneToOneField("Game", on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
