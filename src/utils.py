import os
from datetime import datetime

import dropbox
import requests
from streamlit.uploaded_file_manager import UploadedFile

import constants as const


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
    Upload data to dropbox
    :param file: streamlit UploadedFile
    :return: None
    """

    client = dropbox.dropbox_client.Dropbox(os.environ["UPLOAD_TOKEN"])
    client.files_upload(f=file.getvalue(),
                        path=f"/{get_datetime()}_{file.name}",
                        mode=dropbox.files.WriteMode("overwrite")
                        )
