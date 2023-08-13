from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

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
        def s3_upload(uploaded_file: UploadedFile, key: str, content_type="") -> str:
            """
                Upload a file on Amazon S3, but do not return a File model object.
                Memory/file management is left to the user.
                Please make sure to call delete when the object is no longer
                needed and referencable.
            """
            s3 = boto3_client("s3")
            bucket = get_bucket_name()
            base_url = get_base_url()

            if content_type == "":
                content_type = derive_mime_type_from_ext(uploaded_file.name)

            s3.upload_fileobj(uploaded_file, bucket, key, ExtraArgs={"ContentType": content_type})

            return f"{base_url}{bucket}/{key}"

        @staticmethod
        def s3_delete(key: str):
            """
                Delete a file on Amazon S3
            """
            if not key: return

            s3 = boto3_client("s3")
            bucket = get_bucket_name()

            s3.delete_object(Bucket=bucket, Key=key)

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
            url = File.helpers.s3_upload(uploaded_file, key, content_type)

            return File.objects.create(url=url, key=key,
                                       mime_type=uploaded_file.content_type,
                                       filename=uploaded_file.name)



@receiver(pre_delete, sender=File)
def _delete_file(sender, instance: File, **kwargs):
    """
        This callback deletes the file from Amazon S3 right before its File Model gets destroyed
    """
    File.helpers.s3_delete(instance.key)


def derive_mime_type_from_ext(ext: str) -> str:
    """
        Amazon S3 doesn't automatically add this to files,
        so we need to find & add this manually on our end when uploading.
    """
    match ext:
        case ".aac":  # AAC audio
            content_type = "audio/aac"
        case ".abw":  # abiword document
            content_type = "application/x-abiword"
        case ".aiff": # audio interchange file format
            content_type = "audio/x-aiff"
        case ".arc":  # archive document (multiple files embedded)
            content_type = "application/x-freearc"
        case ".avif": # avif image
            content_type = "image/avif"
        case ".avi":  # avi: audio video interleave
            content_type = "video/x-msvideo"
        case ".azw":  # Amazon Kindle eBook format
            content_type = "application/vnd.amazon.ebook"
        case ".bin":  # any kind of binary data
            content_type = "application/octet-stream"
        case ".bmp":  # Windows os bitmap graphics
            content_type = "image/bmp"
        case ".bz":   # bzip archive
            content_type = "application/x-bzip"
        case ".bz2":  # bzip2 archive
            content_type = "application/x-bzip2"
        case ".cda":  # cd audio
            content_type = "application/x-cdf"
        case ".csh":  # c-shell script
            content_type = "application/x-csh"
        case ".css":  # cascading style sheets (CSS)
            content_type = "text/css"
        case ".csv":  # comma-separated values
            content_type = "text/csv"
        case ".doc":  # Microsoft Word
            content_type = "application/msword"
        case ".docx": # Microsoft Word (OpenXML)
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        case ".eot":  # MS Embedded OpenType fonts
            content_type = "application/vnd.ms-fontobject"
        case ".epub": # electronic publication (EPUB)
            content_type = "application/epub+zip"
        case ".flac": # native flac audio format
            content_type = "audio/x-flac"
        case ".gz":   # GZip compressed archive
            content_type = "application/gzip"
        case ".gif":  # graphics interchange format (GIF)
            content_type = "image/gif"
        case ".htm" | ".html":  # Hypertext Markup Language (HTML)
            content_type = "text/html"
        case ".ico":  # icon format
            content_type = "image/vnd.microsoft.icon"
        case ".ics":  # icalendar format
            content_type = "text/calendar"
        case ".jar":  # java archive
            content_type = "application/java-archive"
        case ".jpeg" | ".jpg":  # jpeg images
            content_type = "image/jpeg"
        case ".js":   # javascript file
            content_type = "text/javascript"
        case ".json": # json format
            content_type = "application/json"
        case ".jsonld": # json-ld format
            content_type = "application/ld+json"
        case ".mid" | ".midi": # musical instrument digital interface (MIDI)
            content_type = "audio/midi"
        case ".mjs":  # javascript module
            content_type = "text/javascript"
        case ".mp3":  # mp3 audio
            content_type = "audio/mpeg"
        case ".mp4":  # mp4 video
            content_type = "video/mp4"
        case ".mpeg": # mpeg video
            content_type = "video/mpeg"
        case ".mpkg": # Apple installer package
            content_type = "application/vnd.apple.installer+xml"
        case ".odp":  # OpenDocument presentation document
            content_type = "application/vnd.oasis.opendocument.presentation"
        case ".ods":  # OpenDocument spreadsheet document
            content_type = "application/vnd.oasis.opendocument.spreadsheet"
        case ".odt":  # OpenDocument text document
            content_type = "application/vnd.oasis.opendocument.text"
        case ".oga" | ".ogg":  # OGG audio
            content_type = "audio/ogg"
        case ".ogv":  # OGG video
            content_type = "video/ogg"
        case ".ogx":  # OGG
            content_type = "application/ogg"
        case ".opus": # Opus audio
            content_type = "audio/opus"
        case ".otf":  # open type font format
            content_type = "font/otf"
        case ".png":  # portable network graphics
            content_type = "image/png"
        case ".pdf":  # Adobe portable document format
            content_type = "application/pdf"
        case ".php":  # hypertext preprocessor
            content_type = "application/x-httpd-php"
        case ".ppt":  # Microsoft PowerPoint
            content_type = "application/vnd.ms-powerpoint"
        case ".pptx": # Microsoft PowerPoint (OpenXml)
            content_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        case ".rar":  # RAR archive
            content_type = "application/vnd.rar"
        case ".rtf":  # rich text format (RTF)
            content_type = "application/rtf"
        case ".sh":   # bourne shell script
            content_type = "application/x-sh"
        case ".svg":  # scalable vector graphics
            content_type = "image/svg+xml"
        case ".tar":  # tape archive (TAR)
            content_type = "application/x-tar"
        case ".tif" | ".tiff": # tagged image file format
            content_type = "image/tiff"
        case ".ts":   # MPEG transport stream
            content_type = "video/mp2t"
        case ".ttf":  # TrueType Font
            content_type = "font/ttf"
        case ".txt":  # plain text (generally ASCII or ISO 8859-n)
            content_type = "text/plain"
        case ".vsd":  # Microsoft VISIO
            content_type = "application/vnd.visio"
        case ".wav":  # waveform audio format (RIFF)
            content_type = "audio/wav"
        case ".weba": # WEBM audio
            content_type = "audio/webm"
        case ".webm": # WEBM video
            content_type = "video/webm"
        case ".webp": # WEBM image
            content_type = "image/webp"
        case ".woff": # Web Open Font Format (WOFF)
            content_type = "font/woff"
        case ".woff2": # Web Open Font Format (WOFF)
            content_type = "font/woff2"
        case ".xhtml": # XHTML
            content_type = "application/xhtml+xml"
        case ".xls":  # Microsoft Excel
            content_type = "application/vnd.ms-excel"
        case ".xlsx": # Microsoft Excel (OpenXML)
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        case ".xml":  # XML
            content_type = "application/xml"
        case ".xul":  # XUL
            content_type = "application/vnd.mozilla.xul+xml"
        case ".zip":  # ZIP archive
            content_type = "application/zip"
        case ".3gp":  # 3gpp audio/video container
            content_type = "video/3gpp" # "audio/3gpp" if audio-only
        case ".3g2":  # 3gpp2 audio/video container
            content_type = "video/3gpp2" # "audio/3gpp2" if audio-only
        case ".7z":   # 7-zip archive
            content_type = "application/x-7z-compressed"
        case _:
            content_type = "application/octet-stream"

    return content_type