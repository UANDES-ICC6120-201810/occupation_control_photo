#!/usr/bin/python
import cv2
import numpy
import os
import sys
import datetime
from uuid import getnode as get_mac


DEFAULT_IMG_FOLDER = '/home/pi/img_folder'


def main(URL=None, path=None):
    if URL is None:
        print "None URL"
        exit(1)
    if path is None:
        path = DEFAULT_IMG_FOLDER
    cam = cv2.VideoCapture(URL)
    ret, frame = cam.read()
    if frame is None:
        print "None frame"
        exit(1)
    h, w, c = frame.shape
    if h <= 0 or w <= 0:
        print "frame size 0"
        exit(1)
    
    if not os.path.exists(path):
        os.makedirs(path)

    mac = get_mac()
    date = datetime.datetime.now()
    img_name = '{}/{}_{}.png'.format(path, mac, date.strftime('%Y%m%d%H%M'))
    try:
        cv2.imwrite(img_name, frame)
    except:
        print "Could not write file"
        exit(1)
    cam.release()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "required at least one arg"
        exit(1)
    else:
        URL = sys.argv[1]
        path = None
        if len(sys.argv) == 3:
            path = sys-argv[2]
        main(URL=URL, path=path)
    print "OK"
    exit(0)
