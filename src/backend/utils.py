import glob
import os
from datetime import datetime
from typing import Union, Optional

import dropbox
import requests
from PIL import Image, UnidentifiedImageError
from PIL.JpegImagePlugin import JpegImageFile
from streamlit.uploaded_file_manager import UploadedFile

from backend import config as conf


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


def download_weights(model_path: Optional[str] = None) -> None:
    """
    Download ONNX weights if necessary
    :return: None
    """
    if model_path is None:
        model_path = os.path.join("backend", "onnx_model")
    os.makedirs(model_path, exist_ok=True)
    for name in conf.gen_config.models_names:
        if name not in os.listdir(model_path):
            r = requests.get(conf.gen_config.download_url + name)
            open(os.path.join(model_path, name), 'wb').write(r.content)


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
    if os.environ.get("DROPBOX_UPLOAD"):
        dropbox_upload(file=file)
    else:
        check_folder(path=conf.gen_config.docker_upload_path)
        try:
            with open(os.path.join(conf.gen_config.docker_upload_path, f"{get_datetime()}_{file.name}"), 'wb') as f:
                f.write(file.getvalue())
        except FileNotFoundError:
            if conf.gen_config.test_upload_path:
                with open(os.path.join(conf.gen_config.test_upload_path, f"{get_datetime()}_{file.name}"), 'wb') as f:
                    f.write(file.getvalue())


def get_mb_folder_size(folder_path: str) -> float:
    """
    Evaluate folder filesize in Mb
    :param folder_path: str
    :return: float
    """
    directory_size = 0.0
    for (path, dirs, files) in os.walk(folder_path):
        for file in files:
            filename = os.path.join(path, file)
            directory_size += os.path.getsize(filename)
    return directory_size / (1024 ** 2)


def check_folder(path: str) -> None:
    """
    Check save folder and clear it if necessary
    :param path: str
    :return: None
    """

    mbs = get_mb_folder_size(path)
    if mbs > conf.gen_config.upload_folder_mb_limit:
        files = glob.glob(os.path.join(path, "*"))
        for f in files:
            os.remove(f)
