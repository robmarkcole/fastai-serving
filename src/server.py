import sys
import json
from base64 import b64encode, b64decode
from io import BytesIO

import aiohttp
import asyncio
import uvicorn
import torch
# from fastai.vision.core import image2tensor, load_learner
from fastai.vision.all import *
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from PIL import Image
import numpy as np

# TODO: improve this hack
# This is used for making additional functions available prior to loading the model.
# For example, you may need a non-fastai defined metric like IOU. You can add that
# function to a utils.py script in a utils folder along with `__init__.py`. Then build with
# docker build --build-arg MODEL_DIR=./model_dir --build-arg UTILS_DIR=./utils -t org/image:tag .`

try:
    from utils.utils import *
    print('loading additional functions from mounted utils directory')
except ModuleNotFoundError as e:
    print('no utils file found, proceeding normally')


app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])

async def setup_learner():
    learner = load_learner('model/export.pkl')
    return learner

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learner = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/analyze:predict', methods=['POST'])
async def analyze(request):
    data = await request.body()
    img_bytes = b64decode(json.loads(data.decode('utf-8'))['image_bytes'])
    img = Image.open(BytesIO(img_bytes))
    prediction = learner.predict(np.array(img))[0]
    return JSONResponse(dict(prediction=prediction))

@app.route('/analyze', methods=['GET'])
def status(request):
    return JSONResponse(dict(status='OK'))

if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=8501, log_level="info")
