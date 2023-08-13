from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

from main_app.models.helpers import derive_mime_type_from_ext
from main_app.util.s3 import get_bucket_name, boto3_client, get_base_url


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


    key = models.URLField(default="")
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


    created_at = models.DateTimeField(default=timezone.now)
    """
        date that the file was uploaded
    """


    # ===== functions =========================================================


    def __repr__(self):
        return f"{self.filename}, created {self.created_at}"


    def __str__(self):
        return self.__repr__()

    class helpers:
        @staticmethod
        def create_and_upload(uploaded_file: UploadedFile, key: str, content_type="") -> "File":
            """
                Uploads a file on Amazon S3, returning its file model object
                Args:
                    uploaded_file: the file to upload, retrieved from `request.FILES`
                    key: the path to append to the base_url to upload the file to.
                        e.g. "users/1/games/17/screenshots/xyz_my_file.png"
                    content_type: adds specific mime type; left blank, it will be derived
                        from the file's extension
                Returns:
                    created File object
            """
            s3 = boto3_client("s3")
            bucket = get_bucket_name()
            base_url = get_base_url()

            if content_type == "":
                content_type = derive_mime_type_from_ext(uploaded_file.name)

            s3.upload_fileobj(uploaded_file, bucket, key, ExtraArgs={"ContentType": content_type})

            url = f"{base_url}{bucket}/{key}"

            return File.objects.create(url=url, key=key,
                                       mime_type=uploaded_file.content_type,
                                       filename=uploaded_file.name)



@receiver(pre_delete, sender=File)
def delete_file(sender, instance: File, **kwargs):
    """This callback deletes the file from Amazon S3 right before its File Model gets destroyed"""
    # raise Exception("delete_file is not implemented")
