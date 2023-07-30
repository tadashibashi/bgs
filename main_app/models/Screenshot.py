from django.db import models
from . import File, Game

class Screenshot(models.Model):
    """
        Screenshot for a game
    """

    file = models.OneToOneField(File, on_delete=models.DO_NOTHING)
    """Associated image file"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    """Associated game"""

    def delete(self, *args, **kwargs):
        """Clean up file when screenshot is deleted"""
        self.file.delete()
        return super(self.__class__, self).delete(*args, **kwargs)
