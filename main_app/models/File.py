from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class File(models.Model):
    """
        The File model represents a persistent file. In the case of our app, Amazon S3 is the backend
        file host.
    """

    filename = models.CharField(max_length=64)
    """name of the file uploaded by the user, stored for human-readable debugging"""

    file_url = models.URLField()
    """Contains the destination file path without the website portion"""

    url = models.URLField()
    """Amazon S3 url. It may be memory-efficient to construct this value with a function via file_url instead."""

    mime_type = models.CharField(max_length=64)
    """file mime type, stored just in case"""

    created_at = models.DateTimeField(auto_now_add=True)
    """date created"""

@receiver(pre_delete, sender=File)
def delete_file(sender, instance: File, **kwargs):
    """This callback deletes the file from Amazon S3 right before its File Model gets destroyed"""
    pass
