from django.db import models

class Tag(models.Model):
    text = models.CharField(64)