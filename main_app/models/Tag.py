from django.db import models

class Tag(models.Model):
    """
        Hashtag for searching for games
    """

    # ===== fields ============================================================


    text = models.CharField(64)


    # ===== functions =========================================================


    def __repr__(self):
        return f"#{self.text}"

    def __str__(self):
        return self.__repr__()
