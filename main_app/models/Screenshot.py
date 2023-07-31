from django.db import models
from . import File, Game

class Screenshot(models.Model):
    """
        Model representing a screenshot image file for a game
    """

    # ===== fields ============================================================


    file = models.OneToOneField(File, on_delete=models.DO_NOTHING)
    """
        The associated image File
        Relationship: Screenshot ---- File

        on_delete:
        When the Screenshot is deleted, we also want to delete its
        corresponding File. `on_delete` is set to `DO_NOTHING`, because there
        is no built-in method for the child to delete its parent on_delete.
        So the desired behavior is manually executed in `Screenshot.delete`.
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    """
        The associated Game that owns this Screenshot
        Relationship: Screenshot >--- Game
    """


    # ===== functions =========================================================


    def delete(self, *args, **kwargs):
        """Clean up File when screenshot is deleted"""
        self.file.delete()

        # perform inherited delete
        return super(self.__class__, self).delete(*args, **kwargs)


    def __repr__(self) -> str:
        """Human-readable string representation"""
        return f"for {self.game.title} @{self.file.filename}"


    def __str__(self) -> str:
        return self.__repr__()
