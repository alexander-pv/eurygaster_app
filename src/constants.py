import os

binary_model_hash = "7dea07bbbad4bc69a33be5768672cb40ef60c344"
multiclass_model_hash = "7e474b5aec7d7cf0b779c969307cd0997f6708aa"

download_url = "https://github.com/alexander-pv/eurygaster_app/releases/download/v1.1.0/"
models_names = [f"model_{binary_model_hash}_binary_calib.onnx",
                f"model_{multiclass_model_hash}_multiclass_calib.onnx"
                ]

onnx_bin_config = {"onnx_model": f"model_{binary_model_hash}_binary_calib.onnx",
                   "class_map": {0: "Eurygaster",
                                 1: "Non_Eurygaster"
                                 },
                   }

onnx_eurg_config = {"onnx_model": f"model_{multiclass_model_hash}_multiclass_calib.onnx",
                    "class_map": {0: "Eurygaster_austriaca",
                                  1: "Eurygaster_dilaticollis",
                                  2: "Eurygaster_integriceps",
                                  3: "Eurygaster_laeviuscula",
                                  4: "Eurygaster_latus",
                                  5: "Eurygaster_maura",
                                  6: "Eurygaster_testudinaria"
                                  },
                    }
image_size = 300
img_normalize = {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}

upload_images = True
upload_folder_mb_limit = 10240
docker_upload_path = os.path.join("/", "app", "uploads")
