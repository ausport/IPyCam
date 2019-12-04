import numpy as np
import cv2

cap_receive = cv2.VideoCapture(
	'xlnxvideosrc src-type=mipi ! video/x-raw, width=1920, height=1080, format=YUY2, framerate=60/1! videoconvert ! appsink',
	cv2.CAP_GSTREAMER)
out_send = cv2.VideoWriter(
	'appsrc ! videoconvert ! xlnxvideosink sink-type="dp" plane-id=34 sync=false fullscreen-overlay=true',
	cv2.CAP_GSTREAMER, 0, 60, (1920, 1080), True)

while True:
	if not cap_receive.isOpened():
		print('VideoCapture not opened')
		exit(0)

	ret, frame = cap_receive.read()

	if not ret:
		print('empty frame')
		continue

	print('received image')
	out_send.write(frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap_receive.release()
out_send.release()