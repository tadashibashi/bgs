from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .Tag import Tag

class Game(models.Model):
    """
        A model representing user-uploaded games
    """

    # ===== fields ============================================================


    url = models.URLField(default="")
    """
        url to the folder on Amazon S3
    """


    title = models.CharField(max_length=128, default="")
    """
        displayable name of the game
    """


    description = models.TextField(default="")
    """
        game description 
    """


    tags = models.ManyToManyField(Tag)
    """
        list of tags to be used for search purposes
    """


    times_viewed = models.IntegerField(default=0)
    """
        number of times a visitor has viewed the game's page
        TODO: Move this to a metrics model?
    """


    is_published = models.BooleanField(default=False)
    """
        whether user has published this game for public viewing
    """


    frame_width = models.IntegerField(default=640)
    """
        width of the iframe, a value of -1 will use the entire view width
    """


    frame_height = models.IntegerField(default=480)
    """
        height of the iframe, a value of -1 will use the entire view height
    """


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """
        creator of the game
    """


    created_at = models.DateTimeField(default=timezone.now)


    updated_at = models.DateTimeField(default=None, blank=True, null=True)


    # ===== functions =========================================================

    def save(self):
        self.updated_at = timezone.now()

        return super().save()

    def __repr__(self) -> str:
        """human-readable string representation"""
        return f"{self.title} by {self.user.username}"

    def __str__(self) -> str:
        return self.__repr__()
