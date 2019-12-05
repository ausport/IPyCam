import numpy as np
import cv2
import sys
import os
import time
os.environ["GST_PLUGIN_PATH"] = "/usr/local/lib/gstreamer-1.0"


_width = 600
_height = 600

#gst-launch-1.0 aravissrc camera-name="JAI Corporation-WU240330" ! video/x-bayer,format=rggb,width=1936,height=1216,framerate=25/1 ! bayer2rgb ! videoconvert ! avenc_mjpeg ! filesink location=frame.jpeg  -v

cap_receive = cv2.VideoCapture(
	'aravissrc camera-name="JAI Corporation-WU240330" ! video/x-bayer, format=rggb, width={0},height={1}, framerate=150/1 ! bayer2rgb ! videoconvert ! appsink'.format(_width, _height),
	cv2.CAP_GSTREAMER)

out_send = cv2.VideoWriter(
	'appsrc ! videoconvert ! xlnxvideosink sink-type="dp" plane-id=34 sync=false fullscreen-overlay=true',
	cv2.CAP_GSTREAMER, 0, 60, (1920, 1080), True)

_t = time.time()
for i in range(0, 100):
	if not cap_receive.isOpened():
		print('VideoCapture not opened')
		exit(0)

	ret, frame = cap_receive.read()

	if not ret:
		print('empty frame')
		continue

	# print('received image {0}'.format(i))
	# out_send.write(frame)
_t = time.time() - _t
_fps = 100. / _t

print("Harvested {0} in {1:04f} seconds.  {2:04f} f.p.s.".format(i+1, _t, _fps))


sys.exit(1)
# cap_receive.release()
# out_send.release()