from django.contrib.auth.models import User
from django.db import models

from .Tag import Tag

class Game(models.Model):
    """
        A model representing user-uploaded games
    """

    url = models.URLField()
    """Base url to the folder in Amazon S3"""


    title = models.CharField(max_length=128, default="")
    """Displayable name of the game"""


    description = models.TextField(default="")
    """Game description that appears underneath game on its detail page."""


    tags = models.ManyToManyField(Tag)
    """Used for search purposes"""


    times_viewed = models.IntegerField(default=0)
    """Number of times a visitor has viewed the game's page. TODO: Move this to a metrics model?"""


    is_published = models.BooleanField(default=False)
    """Whether user has published this game for public viewing"""


    frame_width = models.IntegerField(default=640)
    """Width of the iframe, a value of -1 will use the entire view width"""


    frame_height = models.IntegerField(default=480)
    """Height of the iframe, a value of -1 will use the entire view height"""


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """Creator of the game"""


    created_at = models.DateTimeField(auto_now_add=True)

