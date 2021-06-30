"""Image compressor library using Pillow."""


import glob
import os
from PIL import Image
import time
from werkzeug.datastructures import FileStorage
from . import s3uploader


AWS_S3_IMAGE_BUCKET = 'secretairbucket'

def GetFileExtension(filename: str) -> tuple:
    if '.' in filename:
        file_details = filename.rsplit('.', 1)
        return  file_details[0], file_details[1].lower()
    return filename, None


def IsAllowedFile(filename: str, allowed_types: list):
    return GetFileExtension(filename)[1] in allowed_types


class FileTypeError(Exception):
    pass


class ImageFile(object):

    thumbnail_width = 200
    detail_width = 600
    allowed_types = {'png', 'jpg', 'jpeg'}

    def __init__(self, path: str, file: FileStorage):
        if not IsAllowedFile(file.filename, self.allowed_types):
            raise FileTypeError('Only images %s are allowed.' % self.allowed_types)

        name, img_type = GetFileExtension(file.filename)
        new_name = str(int(time.time() * 1000000)) + '.' + img_type

        self.file = file
        self.new_name = os.path.join(path, new_name)
        self.thumbnail_name = os.path.join(path, 'thumbnails', new_name)

    def _Resize(self, base_width: float) -> Image:
        """Resizes image file."""
        img = Image.open(self.file)
        dimention = img.size
        ratio = self.thumbnail_width / float(dimention[0])
        hsize = int((float(dimention[1]) * float(ratio)))
        img.resize((self.thumbnail_width, hsize), Image.ANTIALIAS)
        return img

    def StandardSize(self, width: int=None, height: int=None) -> str:
        """Compresses images.
        
        Args:
            width: image width in pixels.
            heigth: image height in pixels.

        Returns:
            Image new file name.

        """        
        img = self._Resize(self.detail_width)
        img.save(self.new_name, optimize=True, quality=50)
        s3uploader.UploadFile(filename=self.new_name, bucket=AWS_S3_IMAGE_BUCKET)
        return self.new_name

    def Thumbnail(self) -> str:
        """Creates a thumbnail size to the given image.

        Returns:
            Image new file name.

        """
        img = self._Resize(self.thumbnail_width)

        # Save thumbnail as new image file.
        img.save(self.thumbnail_name, optimize=True, quality=20)
        s3uploader.UploadFile(filename=self.thumbnail_name, bucket=AWS_S3_IMAGE_BUCKET)
        return self.thumbnail_name
