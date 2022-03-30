import glob
import os
from datetime import datetime
from io import BytesIO
from typing import Optional

import dropbox
import requests
from PIL import Image

import config as conf


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


def upload_dropbox(file: bytes, name: str) -> None:
    """
    Upload image to dropbox
    :param file: file in bytes
    :param name filename
    :return: None
    """

    client = dropbox.dropbox_client.Dropbox(os.environ["UPLOAD_TOKEN"])
    client.files_upload(f=file,
                        path=f"/{get_datetime()}_{name}",
                        mode=dropbox.files.WriteMode("overwrite")
                        )


async def upload_image(file: bytes, name: str) -> None:
    """
    Save image to a specified directory
    :param file: image in bytes
    :param name filename
    :return: None
    """
    if conf.gen_config.upload_images:
        if os.environ.get("DROPBOX_UPLOAD"):
            upload_dropbox(file=file, name=name)
        else:
            check_folder(path=conf.gen_config.docker_upload_path)
            try:
                with open(os.path.join(conf.gen_config.docker_upload_path, f"{get_datetime()}_{name}"), 'wb') as f:
                    f.write(file)
            except FileNotFoundError:
                if conf.gen_config.test_upload_path:
                    with open(os.path.join(conf.gen_config.test_upload_path, f"{get_datetime()}_{name}"), 'wb') as f:
                        f.write(file)


def read_image(file: bytes) -> Image.Image:
    """
    Read PIL image from bytes
    :param file: bytes
    :return: Image.Image
    """""
    image = Image.open(BytesIO(file))
    return image


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
