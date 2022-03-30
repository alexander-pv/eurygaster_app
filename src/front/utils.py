from typing import Union

from PIL import Image, UnidentifiedImageError
from PIL.JpegImagePlugin import JpegImageFile
from streamlit.uploaded_file_manager import UploadedFile


def open_image(file: UploadedFile) -> Union[JpegImageFile, None]:
    """
    Open an image with PIL.Image
    :param file: streamlit UploadedFile
    :return: JpegImageFile or None
    """

    try:
        img = Image.open(file)
    except UnidentifiedImageError:
        img = None
    return img
