"""Perform processing of test images."""
import pprint
import requests
import base64

SERVER_URL = "http://localhost:8501/"

### Healthcheck
response = requests.get(
    SERVER_URL + "analyze",
)
if response.status_code == 200:
    print("Server is running")
else:
    print("Server is not running")
    print(response.status_code)

TEST_IMG = "test_img.png"
image_data = open(TEST_IMG, "rb").read()
# print(f"Image {TEST_IMG} data len: {len(image_data)}")

base64_img = base64.b64encode(image_data).decode("utf-8")

response = requests.post(
    SERVER_URL + "analyze:predict",
    json={"image_bytes": base64_img},
)
print(response.status_code)

if response.status_code == 200:
    pprint.pprint(response.json())
else:
    print(response.text)