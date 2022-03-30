import logging
import sys

import uvicorn
from fastapi import FastAPI
from fastapi import File, UploadFile, Body

import config as conf
import model_inference
import utils

app = FastAPI()
eurygaster_models = model_inference.EurygasterModels(models_config=(conf.bm_conf, conf.mm_conf))


@app.get("/")
def read_root() -> dict:
    return {"binary": 'binary_output', 'multiclass': 'multiclass_output'}


@app.post("/predict/eurygaster")
async def predict_eurygaster(file: UploadFile = File(...), name: str = Body(..., embed=True)) -> dict:
    image_bytes = await file.read()
    image = utils.read_image(image_bytes)
    await utils.upload_image(image_bytes, name)
    out = eurygaster_models(image)
    msg = {"binary": out[0], 'multiclass': out[1]}
    logging.info(f'Backend output: {msg}')
    return msg


def main() -> None:
    utils.download_weights()
    uvicorn.run("inference_server:app",
                host=conf.gen_config.server_host,
                port=conf.gen_config.server_port,
                debug=conf.gen_config.debug)


if __name__ == "__main__":
    sys.exit(main())
