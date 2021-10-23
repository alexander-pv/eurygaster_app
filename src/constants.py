onnx_bin_config = {"onnx_model": "mobilenet_v2_7dea07bbbad4bc69a33be5768672cb40ef60c344_epoch_55_calib.onnx",
                   "class_map": {0: "Eurygaster",
                                 1: "Non_Eurygaster"
                                 },
                   }

onnx_eurg_config = {"onnx_model": "mobilenet_v2_7e474b5aec7d7cf0b779c969307cd0997f6708aa_epoch_81_calib.onnx",
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
