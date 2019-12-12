import numpy as np
import cv2
import sys
import os
import time
os.environ["GST_PLUGIN_PATH"] = "/usr/local/lib/gstreamer-1.0"


_width = 1936
_height = 1216
_frame_rate = 50
frame = None

#gst-launch-1.0 aravissrc camera-name="JAI Corporation-WU240330" ! video/x-bayer,format=rggb,width=1936,height=1216,framerate=25/1 ! bayer2rgb ! videoconvert ! avenc_mjpeg ! filesink location=frame.jpeg  -v

cap_receive = cv2.VideoCapture(
	'aravissrc camera-name="JAI Corporation-WU240330" ! video/x-bayer, format=rggb, width={0},height={1}, framerate={2}/1 ! bayer2rgb ! videoconvert ! appsink'.format(_width, _height, _frame_rate),
	cv2.CAP_GSTREAMER)

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out_send = cv2.VideoWriter('output3.mp4', fourcc, _frame_rate, (_width, _height))

_t = time.time()
for i in range(0, _frame_rate*5):
	if not cap_receive.isOpened():
		print('VideoCapture not opened')
		exit(0)

	ret, frame = cap_receive.read()

	if not ret:
		print('empty frame')
		continue

	# out_send.write(frame)

_t = time.time() - _t
_fps = (_frame_rate*5.) / _t

print("Harvested {0} frames in {1:04f} seconds.  {2:04f} f.p.s.".format(i+1, _t, _fps))

sys.exit(1)
# cap_receive.release()
# out_send.release()