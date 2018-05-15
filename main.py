import cv2
import numpy

URL = "rtsp://192.168.1.92:554"
cam = cv2.VideoCapture(URL)
i = 0
file_generic_name = 'saved{}'
while True:
    ret, frame = cam.read()
    try:
        cv2.imshow('frame', frame)
    except Exception:
        print "Could not load frame, re-establishing connection"
        cam.release()
        print "camera connetion released"
        cam = cv2.VideoCapture(URL)
        print "camera connection established"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        saved_file_name = '{}.png'.format(file_generic_name.format(i))
        cv2.imwrite(saved_file_name, frame)
        i += 1
        print 'image saved as {}'.format(saved_file_name)

cam.release()
cv2.destroyAllWindows()
