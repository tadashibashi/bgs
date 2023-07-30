from django.db import models
from . import File, Game

class Screenshot(models.Model):
    """
        Model representing a screenshot image file for a game
    """

    file = models.OneToOneField(File, on_delete=models.DO_NOTHING)
    """
        The associated image File
        Relationship: Screenshot ---- File

        on_delete:
        When the Screenshot is deleted, we also want to delete its corresponding
        File. `on_delete` is set to `DO_NOTHING`, because there is no built-in method where 
        the child deletes the parent when deleted.
        We manually set the desired behavior in the overridden `Screenshot.delete` def.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    """
        The associated Game that owns this Screenshot
        Relationship: Screenshot >--- Game
    """

    def delete(self, *args, **kwargs):
        """Clean up File when screenshot is deleted"""
        self.file.delete()

        # perform inherited delete
        return super(self.__class__, self).delete(*args, **kwargs)
