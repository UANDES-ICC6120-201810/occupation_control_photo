#!/usr/bin/python
import cv2
import numpy
import os
import sys
import datetime
import boto3
from uuid import getnode as get_mac


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
    img_file = '{mac}_{date}.png'.format(mac=mac, date=date.strftime('%Y%m%d%H%M'))
    img_path = '{directory}/{file}'.format(directory=directory, file=img_file)
    try:
        cv2.imwrite(img_path, frame)
    except:
        print "Could not write file"
        exit(1)
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://zapo-storage.nyc3.digitaloceanspaces.com',
                            aws_access_key_id='JBLMV4KWTMQFT6REUZ2Z',
                            aws_secret_access_key='jj/3LqrpnS9EAQQYNHHY536u8we9ugQOBcTOG+7E/Cs')
    client.upload_file(img_path,
                       'zapo-storage',
                       img_file)
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
