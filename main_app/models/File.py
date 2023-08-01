import datetime

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class File(models.Model):
    """
        This model represents a persistent file.
        In the case of our app, Amazon S3 is the backend file host.
    """

    # ===== fields ============================================================


    filename = models.CharField(max_length=64, default="")
    """
        name from user upload
    """


    file_url = models.URLField(default="")
    """
        contains the destination filepath without the website root
    """


    url = models.URLField(default="")
    """
        Amazon S3 url
    """


    mime_type = models.CharField(max_length=64, default="")
    """
        file type
    """


    created_at = models.DateTimeField(default=datetime.datetime.now)
    """
        date that the file was uploaded
    """


    # ===== functions =========================================================


    def __repr__(self):
        return f"{self.filename}, created {self.created_at}"


    def __str__(self):
        return self.__repr__()



@receiver(pre_delete, sender=File)
def delete_file(sender, instance: File, **kwargs):
    """This callback deletes the file from Amazon S3 right before its File Model gets destroyed"""
    # raise Exception("delete_file is not implemented")
