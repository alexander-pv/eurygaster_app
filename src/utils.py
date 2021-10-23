import os

import requests

import constants as const


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
