#!/usr/bin/python
import cv2
import numpy
import os
import sys
import datetime
import boto3
from uuid import getnode as get_mac
from settings import *


DEFAULT_IMG_FOLDER = '/home/pi/img_folder'


def main(URL=None, directory=None):
    if URL is None:
        print "None URL"
        exit(1)
    if directory is None:
        directory = DEFAULT_IMG_FOLDER
    cam = cv2.VideoCapture(URL)
    ret, frame = cam.read()
    if frame is None:
        print "None frame"
        exit(1)
    h, w, c = frame.shape
    if h <= 0 or w <= 0:
        print "frame size 0"
        exit(1)
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    mac = get_mac()
    date = datetime.datetime.now()
    img_file = '{date}.png'.format(date=date.strftime('%Y%m%d%H%M'))
    img_path = '{directory}/{file}'.format(directory=directory, file=img_file)
    try:
        cv2.imwrite(img_path, frame)
    except:
        print "Could not write file"
        exit(1)
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='{region}'.format(region=AWS_REGION),
                            endpoint_url='https://{bucket}.{url}'.format(bucket=AWS_STORAGE_BUCKET_NAME,
                                                                         url=AWS_S3_ENDPOINT_URL),
                            aws_access_key_id='{access_key}'.format(access_key=AWS_ACCESS_KEY_ID),
                            aws_secret_access_key='{secret_key}'.format(secret_key=AWS_SECRET_ACCESS_KEY))
    client.upload_file(img_path,
                       '{folder}/{mac}'.format(folder=AWS_LOCATION, mac=mac),
                       img_file,
                       ExtraArgs = {'ACL': 'public-read'}) # TODO: Check if last argument is propertly setted
    cam.release()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "required at least one arg"
        exit(1)
    else:
        URL = sys.argv[1]
        directory = None
        if len(sys.argv) == 3:
            directory = sys-argv[2]
        main(URL=URL, directory=directory)
    print "OK"
    exit(0)
