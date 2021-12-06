# fastai serving
A Docker image for serving [fastai](https://www.fast.ai/) models. It is not optimized for performance.

## Build
First, export a fastai `Learner` with [`.export`](https://docs.fast.ai/basic_train.html#Learner.export). Assuming that this file is in `model_dir`, you can build the serving image like so:
```
# docker build -f Dockerfile.[cpu/gpu] --build-arg MODEL_DIR=./model_dir -t fastserve .`
```

If you require additional utils files for loading the model with [`load_learner`](https://docs.fast.ai/basic_train.html#load_learner), you can mount an additional directory at build time with:
```
# docker build -f Dockerfile.[cpu/gpu] --build-arg MODEL_DIR=./model_dir --build-arg UTILS_DIR=./utils -t fastserve .`
```

## Run
```
docker run --rm -p 8501:8501 -t fastserve .
```

## Use
The API currently has two endpoints:

### `POST /analyze:predict`
Accepts a JSON request in the form:

```js
{
      "image_bytes": "[b64_string]"
}
```

where each `b64_string` is a base-64 encoded string representing the model input.

### `GET /analyze`
Returns an HTTP Status of `200` as long as the API is running (health check).

## Example request
Place an image `test_image.png` in the `tests` folder and run the script `tests/test_request.py`. Example output from the script:

```
python3 test_request.py
Server is running
200
{'prediction': 'my_result'}
```

## Note
I had to unpin dependencies in the `Dockerfile.cpu`. I have not tested `Dockerfile.gpu`

## Acknowledgments
- The code for `server.py` is taken almost entirely from the [fastai example](https://github.com/render-examples/fastai-v3) for [Render](https://render.com/). The primary addition is the batch inference code which can provide significant speed-ups compared to single image prediction.
- This work was undertaken in partnership with our friends at [Sinergise](https://www.sinergise.com/) and funded by the [European Space Agency](https://www.esa.int/ESA), specifically [Phi Lab](http://blogs.esa.int/philab/)


