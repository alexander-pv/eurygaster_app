import dataclasses
import os
import platform
from typing import Any, Optional


@dataclasses.dataclass
class GeneralConfig:
    models_names: list or tuple
    server_host: str = '0.0.0.0'
    server_port: int = 15000
    download_url: str = "https://github.com/alexander-pv/eurygaster_app/releases/download/v1.3.0/"
    upload_images: bool = True
    upload_folder_mb_limit: int = 10240
    docker_upload_path: str = os.path.join("/", "app", "uploads")
    test_upload_path: str or None = os.path.join(os.environ["HOME"]) if platform.system() == 'Linux' else None
    debug: bool = False


class ModelConfig:

    def __init__(self, model_hash: str, model_template_name: str, class_map: dict,
                 input_size: int = 300, normalization: Optional[dict] = None):
        """
        :param model_hash:          str, model hash
        :param model_template_name: str, model name without specific hash
        :param class_map:           dict, mapping class id to str
        :param input_size:          int, image input size
        :param normalization:       dict, input image normalization parameters
        """
        self.model_hash = model_hash
        self.model_template_name = model_template_name
        self.model_name = self.get_model_name()
        self.class_map = class_map
        self.input_size = input_size
        self.normalization = self.get_value(normalization,
                                            {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]})

    @staticmethod
    def get_value(param: Any, default: Any) -> Any:
        if not param:
            param = default
        return param

    def get_model_name(self) -> str:
        return self.model_template_name.replace('$hash$', self.model_hash)


bm_conf = ModelConfig(model_hash="0d03affcc3fe4555217e01aee7d73fed7ebdf35a",
                      model_template_name="model_$hash$_binary_calib.onnx",
                      class_map={
                          0: "Eurygaster",
                          1: "Non_Eurygaster"
                      }
                      )
mm_conf = ModelConfig(model_hash="4fa9730aef422d53cf1ccb3db93da78d68991301",
                      model_template_name="model_$hash$_multiclass_calib.onnx",
                      class_map={
                          0: "Eurygaster_austriaca",
                          1: "Eurygaster_dilaticollis",
                          2: "Eurygaster_integriceps",
                          3: "Eurygaster_laeviuscula",
                          4: "Eurygaster_maura",
                          5: "Eurygaster_testudinaria"
                      },
                      )

gen_config = GeneralConfig(models_names=(bm_conf.model_name, mm_conf.model_name))
