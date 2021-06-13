"""Image compressor library using Pillow."""
from PIL import Image
import PIL
import os
import glob
import time


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

    thumnail_width = 300
    allowed_types = {'png', 'jpg', 'jpeg'}

    def __init__(self, path, filename: str):
        if not IsAllowedFile(filename, self.allowed_types):
            raise FileTypeError('Only images %s allowed.' % allowed_types)

        name, img_type = GetFileExtension(filename)
        new_name = str(int(time.time() * 1000000)) + '.' + img_type

        self.filename = os.path.join(path, filename)
        self.new_name = os.path.join(path, new_name)
        self.thumdnail_name = os.path.join(path, 'thumbnails', new_name)


    def StandardSize(self, width: int=None, height: int=None) -> str:
        """Compresses images.
        
        Args:
            filename: image file name.
            width: image width in pixels.
            heigth: image height in pixels.

        Returns:
            Image new file name.

        """        
        img = Image.open(self.filename)
        img.save(self.new_name, optimize=True, quality=50)
        return self.new_name


    def Thumbnail(self) -> str:
        """Creates a thumbnail size to the given image.
        
        Args:
            filename: image file name.

        Returns:
            Image new file name.

        """
        img = Image.open(self.filename)
        dimention = img.size
        ratio = self.thumnail_width / float(dimention[0])
        hsize = int((float(dimention[1]) * float(ratio)))
        img.resize((self.thumnail_width, hsize), Image.ANTIALIAS)

        # Save thumbnail as new image file.
        img.save(self.thumdnail_name, optimize=True, quality=30)
        return self.new_name