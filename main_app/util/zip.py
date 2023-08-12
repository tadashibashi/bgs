

import typing
from zipfile import ZipFile
from pathlib import PurePath

class BgsZipfile:
    """
        Handles a zip file
    """

    def __init__(self):
        self.file: ZipFile|None = None
        self.files: list[typing.BinaryIO] = []

    def __del__(self):
        """
            Cleans up any remaining file in case user forgot to clean up
        """
        self.close()


    def open(self, bytes_or_path):
        try:
            file = ZipFile(bytes_or_path, mode="r")
            result = file.testzip()
            if result is not None:
                print(f"Bad file in zip: {result}")
                file.close()
                return

            self.close()
            self.file = file
            self.__populate_files()

        except Exception as e:
            print("Failed to open zipfile: ", e)


    def is_open(self):
        return self.file is None

    def close(self):
        if self.file and self.file.fp:
            for file in self.files:
                file.close()
            self.files.clear()

            self.file.close()
            self.file = None

    def __populate_files(self):
        if not self.is_open():
            return

        path = PurePath(self.file.filename)
        files = []

        for info in self.file.filelist:
            # get correct files: no folders or system files
            if not info.is_dir() and info.filename.startswith(path.stem):
                files.append(self.file.open(info.filename, "r"))


