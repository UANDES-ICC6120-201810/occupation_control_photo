#!/usr/bin/python
import cv2
import numpy
import os
import sys
import datetime
import time
import boto3
import requests
from uuid import getnode as get_mac
from settings import *


DEFAULT_IMG_FOLDER = '/home/pi/img_folder'


def main(URL=None, directory=None):
    if URL is None:
        print "None URL"
        return
    if directory is None:
        directory = DEFAULT_IMG_FOLDER
    cam = cv2.VideoCapture(URL)
    ret, frame = cam.read()
    if frame is None:
        print "None frame"
        return
    h, w, c = frame.shape
    if h <= 0 or w <= 0:
        print "frame size 0"
        return

    cam.release()

    if not os.path.exists(directory):
        os.makedirs(directory)

    mac = get_mac()
    date = datetime.datetime.now()
    img_file = '{date}.png'.format(date=date.strftime('%Y%m%d%H%M'))
    img_path = '{directory}/{file}'.format(directory=directory, file=img_file)

    # Saving frame
    try:
        cv2.imwrite(img_path, frame)
    except:
        print "Could not write file"
        return

    # Uploading image to digitalocean storage
    try:
        session = boto3.session.Session()
        client = session.client(
            's3',
            region_name='{region}'.format(region=AWS_REGION),
            endpoint_url='https://{bucket}.{url}'.format(
                bucket=AWS_STORAGE_BUCKET_NAME,
                url=AWS_S3_ENDPOINT_URL
            ),
            aws_access_key_id='{access_key}'.format(
                access_key=AWS_ACCESS_KEY_ID
            ),
            aws_secret_access_key='{secret_key}'.format(
                secret_key=AWS_SECRET_ACCESS_KEY
            )
        )
        client.upload_file(img_path,
                       '{folder}'.format(folder=AWS_LOCATION),
                       '{mac}/{filename}'.format(mac=mac, filename=img_file),
                       ExtraArgs = {'ACL': 'public-read'})
    except:
        print "Could not upload to digitalocean spaces."
        return

    # Sending request to API
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJidXNfc3RvcF9jb2RlIjoiUEMxMDQ5In0.ys4OrX8lMe7h3wPIhv5Du7WFUDbxC5fszhumADKdlIc'
    headers = {
        'Authorization': str('Bearer ' + token)
    }
    endpoint_format = 'https://{bucket}.{url}'
    body = {
        'source_endpoint': endpoint_format.format(
            bucket=AWS_STORAGE_BUCKET_NAME,
            url=AWS_S3_ENDPOINT_URL
        ),
        'source_bucket': '{bucket}'.format(bucket=AWS_LOCATION),
        'source_folder': '{mac}'.format(mac=mac),
        'source_filename': '{filename}'.format(filename=img_file)
    }
    response = requests.post(
        url='http://proyectozapo.herokuapp.com/api/v1/occupation_event',
        headers=headers,
        data=body
    )

    if not response.ok:
        print "Could not send request to API: {status}".format(status=response)
        print response.content
        return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "required at least one arg"
        exit(1)
    else:
        URL = sys.argv[1]
        directory = None
        if len(sys.argv) == 3:
            directory = sys.argv[2]
        while True:
            main(URL=URL, directory=directory)
            print "OK"
            time.sleep(60*5)
    exit(0)
