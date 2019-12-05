import numpy as np
import cv2
import sys

#gst-launch-1.0 aravissrc camera-name="JAI Corporation-WU240330" ! video/x-bayer,format=rggb,width=1936,height=1216,framerate=25/1 ! bayer2rgb ! videoconvert ! avenc_mjpeg ! filesink location=frame.jpeg  -v

cap_receive = cv2.VideoCapture(
	'aravissrc camera-name="JAI Corporation-WU240330" ! video/x-bayer, format=rggb, width=1936,height=1216, framerate=150/1 ! bayer2rgb ! videoconvert ! appsink',
	cv2.CAP_GSTREAMER)

out_send = cv2.VideoWriter(
	'appsrc ! videoconvert ! xlnxvideosink sink-type="dp" plane-id=34 sync=false fullscreen-overlay=true',
	cv2.CAP_GSTREAMER, 0, 60, (1920, 1080), True)

print("Trying...")


for i in range(0, 100):
	if not cap_receive.isOpened():
		print('VideoCapture not opened')
		exit(0)

	ret, frame = cap_receive.read()

	if not ret:
		print('empty frame')
		continue

	print('received image {0}'.format(i))
	# out_send.write(frame)


sys.exit(1)
# cap_receive.release()
# out_send.release()