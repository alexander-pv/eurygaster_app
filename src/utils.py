import os
from datetime import datetime
from typing import Union

import dropbox
import requests
from PIL import Image, UnidentifiedImageError
from PIL.JpegImagePlugin import JpegImageFile
from streamlit.uploaded_file_manager import UploadedFile

import constants as const


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


def get_datetime() -> str:
    """
    Get formatted UTC datetime string
    :return: str
    """
    dt = str(datetime.utcnow())[:19]
    for c in [":", "-", " "]:
        dt = dt.replace(c, "_")
    return dt


def download_weights() -> None:
    """
    Download ONNX weights if necessary
    :return: None
    """
    os.makedirs("onnx_model", exist_ok=True)
    for name in const.models_names:
        if name not in os.listdir("onnx_model"):
            r = requests.get(const.download_url + name)
            open(os.path.join("onnx_model", name), 'wb').write(r.content)


def dropbox_upload(file: UploadedFile) -> None:
    """
    Upload image to dropbox
    :param file: streamlit UploadedFile
    :return: None
    """

    client = dropbox.dropbox_client.Dropbox(os.environ["UPLOAD_TOKEN"])
    client.files_upload(f=file.getvalue(),
                        path=f"/{get_datetime()}_{file.name}",
                        mode=dropbox.files.WriteMode("overwrite")
                        )


def image_upload(file: UploadedFile) -> None:
    """
    Save image to a specified directory
    :param file: streamlit UploadedFile
    :return: None
    """
    with open(os.path.join(const.upload_path, f"{get_datetime()}_{file.name}"), 'wb') as f:
        f.write(file.getvalue())
