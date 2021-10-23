import os
from typing import Callable
from typing import Tuple

import numpy as np
import onnxruntime as ort
import torchvision
from PIL.JpegImagePlugin import JpegImageFile
from scipy.special import softmax

import constants as const


class ONNXInference:

    def __init__(self, onnx_model_name: str, input_name: str, output_name: str,
                 preprocess: Callable[[np.array], np.array], class_map: dict):
        """
        Wrapper for ONNX model inference
        :param onnx_model_name:  str, "<model_name>.onnx"
        :param input_name: str
        :param output_name: str
        :param preprocess: function for input transformation, from torchvision.transform
        :param class_map: dict, class mapping: {class_id: class_name, ...}
        """
        self.onnx_model_name = onnx_model_name
        self.input_name = input_name
        self.output_name = output_name
        self.ort_sess = ort.InferenceSession(self.onnx_model_name)
        self.preprocess = preprocess
        self.class_map = class_map

    def run(self, image: JpegImageFile) -> np.array:
        """
        Run onnxruntime inference session
        :param image: Pillow JpegImageFile, image input
        :return:      np.array, softmax output
        """
        input_data = np.expand_dims(self.preprocess(image).numpy(), 0)
        outputs = self.ort_sess.run(output_names=[self.output_name], input_feed={self.input_name: input_data})
        return softmax(outputs).ravel()


def get_input_transform(image_size: int, img_normalize: dict) -> torchvision.transforms.Compose:
    """
    Get torchvision transform pipeline for an input
    :param image_size:    int, image size for resizing
    :param img_normalize: dict with mean and std for image normalization
    :return:
    """
    transform_list = [torchvision.transforms.Resize(size=(image_size, image_size)),
                      torchvision.transforms.ToTensor(),
                      torchvision.transforms.Normalize(mean=img_normalize['mean'], std=img_normalize['std'])]
    return torchvision.transforms.Compose(transform_list)


def get_confidence_dict(class_map: dict, model_output: np.array) -> dict:
    """
    Get confidence dict
    :param class_map: dict
    :param model_output: np.array
    :return:
    """
    conf_dict = dict()
    for i, conf in enumerate(model_output):
        conf_dict.update({class_map[i]: "%.3f" % conf})
    return conf_dict


def do_inference(pil_image: JpegImageFile) -> Tuple[dict, dict]:
    """
    Do the inference
    :param pil_image: JpegImageFile
    :return: dict, dict
    """
    onnx_bin_instance = ONNXInference(
        onnx_model_name=os.path.join("onnx_model", const.onnx_bin_config["onnx_model"]),
        input_name="mobilenetv2_input",
        output_name="mobilenetv2_output",
        preprocess=get_input_transform(image_size=const.image_size, img_normalize=const.img_normalize),
        class_map=const.onnx_bin_config["class_map"]
    )
    bin_result = get_confidence_dict(class_map=const.onnx_bin_config['class_map'],
                                     model_output=onnx_bin_instance.run(image=pil_image))

    onnx_eurg_instance = ONNXInference(
        onnx_model_name=os.path.join("onnx_model", const.onnx_eurg_config["onnx_model"]),
        input_name="mobilenetv2_input",
        output_name="mobilenetv2_output",
        preprocess=get_input_transform(image_size=const.image_size, img_normalize=const.img_normalize),
        class_map=const.onnx_eurg_config["class_map"]
    )
    eurg_result = get_confidence_dict(class_map=const.onnx_eurg_config['class_map'],
                                      model_output=onnx_eurg_instance.run(image=pil_image))
    return bin_result, eurg_result
