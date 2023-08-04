from django.db import models
from django.utils import timezone

from .File import File
from .Game import Game


class Screenshot(models.Model):
    """
        Model representing a screenshot image file for a game
    """

    # ===== metadata ==========================================================



    class Meta:
        ordering = ["created_on"]
        """
            Order by date created.
            Icebox feature: allow user to choose the Screenshot ordering 
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


    created_on = models.DateTimeField(default=timezone.now)


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
