import typing
from zipfile import ZipFile
from pathlib import PurePath
import re

# Regex pattern-matching for undesired files in zip
_IGNORE_LIST = [
    ".*\.DS_Store",
    "Thumbs.db",
    "ehthumbs.*\.db",
]

class BgsZipfile:
    """
        Zip file utility class
    """


    def __init__(self):
        self.file: ZipFile|None = None
        self.files: list[typing.BinaryIO] = []


    def __del__(self):
        """
            Clean up in case user forgets call to close()
        """
        self.close()


    def open(self, bytes_or_path):
        """
            Open a zipfile

            Args:
                bytes_or_path: a buffer or path to a file

            Returns:
                True on successful open, and False on error.
                If an error occurs, internals will not be mutated.
        """

        # open the file
        try:
            file = ZipFile(bytes_or_path, mode="r")
        except Exception as e:
            print("BgsZipfile: failed to open file:", e)
            return False


        try:
            # test for bad files
            result = file.testzip()
            if result is not None:
                print(f"BgsZipFile: bad file in zip: {result}")
                file.close()
                return False

            # clean up old file, if any
            self.close()

            # get files inside zip
            self.files = self.__get_files(file)
            self.file = file

        except Exception as e:
            print("BgsZipFile: failed during open: ", e)
            file.close()
            return False

        return True


    def is_open(self):
        """
            Checks if zip file is open
        """
        return bool(self.file and self.file.fp)


    def close(self):
        """
            Clean up the file. Automatically called during the destructor,
            but best if called when done with the zip file.
            Safe to call even if file is not open.
        """

        # handle & report all exceptions, should not throw
        try:
            if self.is_open():
                for file in self.files:
                    file.close()
                self.files.clear()

                self.file.close()
                self.file = None

        except Exception as e:
            print("BgsZipfile: exception occured during close(): ", e)

    @staticmethod
    def __get_files(zip_file: ZipFile):
        """
            Get the individual files from a zip_file

            Returns: array of file objects
        """
        path = PurePath(zip_file.filename)
        files = []

        for info in zip_file.filelist:
            filepath = PurePath(info.filename)

            # get correct files: no folders or system files
            if (not info.is_dir() and filepath.parts[0] == path.stem and
            not [
                match
                for match in _IGNORE_LIST
                if re.search(match, info.filename)
            ]):
                files.append(zip_file.open(info.filename, "r"))

        return files
