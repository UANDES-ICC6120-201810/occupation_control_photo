import cv2
import requests
import os
from os.path import isfile, join


OCCUPATION_IMAGE_API_URL = ""
API_AUTH_KEY = ""
IMG_PATH = "./buffer"


def main():
    images = [f for f in os.listdir(IMG_PATH) if isfile(join(IMG_PATH, f))]

    headers = {'Authorization': API_AUTH_KEY}
    for img_path in images:
        img_name = img_path.split('/')[-1]
        now = img_name.split('_')[-1]
        data = {'name': img_name, 'datetime': now}
        files = {'file': open(img_path)}
        r = requests.post(OCCUPATION_IMAGE_API_URL,
                          files=files,
                          headers=headers,
                          data=data)

        if r.ok:
            os.remove(img_path)
