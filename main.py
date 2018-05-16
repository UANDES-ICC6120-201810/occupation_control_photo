import cv2
import numpy
import os
import sys
import datetime
from uuid import getnode as get_mac


DEFAULT_IMG_FOLDER = '/home/img_buffer'


def main(URL=None, path=None):
    if URL is None:
        exit(1)
    if path is None:
        path = DEFAULT_IMG_FOLDER
    cam = cv2.VideoCapture(URL)
    ret, frame = cam.read()
    h, w, c = frame.shape
    if h <= 0 or w <= 0:
        exit(1)
    
    if not os.path.exists(path):
        os.makedirs(path)

    mac = get_mac()
    date = datetime.datetime.now()
    img_name = '{}/{}_{}.png'.format(path, mac, date.strftime('%Y%m%d%H%M'))
    try:
        cv2.imwrite(img_name, frame)
    except:
        exit(1)
    cam.release()
    exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(1)
    else:
        URL = sys.argv[1]
        path = None
        if len(sys.argv) == 3:
            path = sys-argv[2]
        main(URL=URL, path=path)

