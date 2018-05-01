import cv2
import requests
import datetime
import os


OCCUPATION_IMAGE_API_URL = ""
API_AUTH_KEY = ""
IMG_BASE_ID = ""


def main():
    cam = cv2.VideoCapture(0)

    img = cam.read()
    now = datetime.datetime.now()
    img_name = '{id}_{date}'.format(id=IMG_BASE_ID, date=now)

    img_path = './buffer/{name}'.format(name=img_name)
    cv2.imwrite(img_path, img)

    headers = {'Authorization': API_AUTH_KEY}
    data = {'name': img_name, 'datetime': now}
    files = {'file': img}
    r = requests.post(OCCUPATION_IMAGE_API_URL,
                      files=files,
                      headers=headers,
                      data=data)

    if r.ok:
        os.remove(img_path)
        return 1
    return 0
