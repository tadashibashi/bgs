import uuid
from pathlib import PurePath

from django.core.files.uploadedfile import UploadedFile
from django.utils.text import slugify

from . import Screenshot, File, Game

def get_fileext(uploaded_file: UploadedFile) -> str:
    if uploaded_file.name:
        return uploaded_file.name[uploaded_file.name.rfind("."):]
    else:
        return ""

def gen_filename(filename: str, prepend_hash=6) -> str:
    """
        Creates valid slugged filename for the web, prepends 6 random characters to
        prevent file name collisions. If no name is provided to uploaded file,
        returns any empty string.
        Args:
            filename: name to alter
            prepend_hash: number of hash characters to prepend filename with
                max is 32 chars, anything 0 or less will not prepend any chars.
        Returns:
            filename string
    """
    if filename:
        prepend_hash = max(prepend_hash, 32)
        hash_str = uuid.uuid4().hex[:prepend_hash] if prepend_hash > 0 else ""
        file_path = PurePath(filename)
        filename = hash_str + slugify(file_path.stem) + file_path.suffix
    else:
        return ""

    return filename

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


#
# TODO: VVV All code below needs to be refactored to allow multiple screenshot files & reordering VVV
#

def create_screenshot(uploaded_file: UploadedFile, game_id: int) -> Screenshot | None:
    """
        Helper function to create a Screenshot from a file
        Url will be "user/<int:user_id>/games/<int:game_id>/screenshots/<6-char hash><filename><ext>"
        Args:
            uploaded_file: the file to upload, retrieved from `request.FILES`
            game_id: the game this screenshot is for
        Returns:
            Created Screenshot object on success, or None if game_id is invalid, or no filename
            retrieved from the `uploaded_file`
    """

    # get game to find user_id
    game = Game.objects.get(id=game_id)
    if not game:
        return None  # not a valid game

    user_id = game.user_id

    # get filename
    filename = gen_filename(uploaded_file.name)
    if not filename:
        return None  # not a valid filename

    # get folder
    folder = "user/" + str(user_id) + "/games/" + str(game_id) + "/screenshots/"

    # create file
    file = File.helpers.create_and_upload(uploaded_file, folder + filename)

    # attach file to new screenshot
    return Screenshot.objects.create(file=file, game_id=game_id)


def update_screenshot(screenshot_id: int, uploaded_file: UploadedFile):
    screenshot = Screenshot.objects.get(id=screenshot_id)

    if not screenshot:
        print("updated_screenshot error: invalid screenshot_id")
        return False  # not a valid screenshot

    # get folder
    folder = ("user/" + str(screenshot.game.user_id) + "/games/" +
              str(screenshot.game_id) + "/screenshots/")

    # get filename
    filename = gen_filename(uploaded_file.name)
    if not filename:
        print("update_screenshot error: failed to get name from uploaded file")
        return False  # not a valid filename

    # create file
    file = File.helpers.create_and_upload(uploaded_file, folder + filename)
    if not file:
        print("update_screenshot error: File failed to create")
        return False  # file failed to create

    # done -- replace file & commit
    screenshot.file.delete()
    screenshot.file = file
    screenshot.save()
    return True


def create_or_update_single_screenshot(uploaded_file: UploadedFile, game_id: int):
    """
        Create or update a Game's single screenshot
    """

    game = Game.objects.get(id=game_id)
    if not game:
        print("create_or_update_single_screenshot error: invalid game_id")
        return False

    if game.screenshot_set.count() > 0:
        screenshot = game.screenshot_set.first()
        screenshot.delete()

    screenshot = create_screenshot(uploaded_file, game_id)
    if not screenshot:
        print("create_or_update_single_screenshot error: failed to create_screenshot")
        return False
    game.screenshot_set.add(screenshot)

    return True