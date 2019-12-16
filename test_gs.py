import numpy as np
import cv2
import sys
import os
import time
os.environ["GST_PLUGIN_PATH"] = "/usr/local/lib/gstreamer-1.0"
# gst-launch-1.0 aravissrc camera-name="JAI Corporation-WU240330" ! video/x-bayer,format=rggb,width=1936,height=1216,framerate=25/1 ! bayer2rgb ! videoconvert ! avenc_mjpeg ! filesink location=frame.jpeg  -v


def do_test(camera, dest_path = None, fps=None, w=None, h=None):

	assert camera is not None, "A camera name must be passed!"

	_width = w or 1936
	_height = h or 1216

	_frame_rate = fps or 50

	cap_receive = cv2.VideoCapture(
		'aravissrc camera-name="{0}" ! video/x-bayer, format=rggb, width={1}, height={2}, framerate={3}/1 ! bayer2rgb ! videoconvert ! appsink'.format(camera, _width, _height, _frame_rate),
		cv2.CAP_GSTREAMER)

	if dest_path is not None:
		fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
		out_send = cv2.VideoWriter(dest_path, fourcc, _frame_rate, (_width, _height))

	print("* * * * * * * * * *")
	print("Running GStreamer Test:")
	print("\tDevice Name:      {0}".format(camera))
	print("\tTarget Rate:      {0} f.p.s".format(_frame_rate))
	print("\tCapture Duration: {0} frames.".format(_frame_rate*5))
	print("\tCapture Path:     {0}.".format(dest_path or "n/a"))
	print("* * * * * * * * * *")

	if not cap_receive.isOpened():
		print('VideoCapture not opened')
		exit(0)

	_t = time.time()
	for i in range(0, _frame_rate*5):

		ret, frame = cap_receive.read()

		if not ret:
			print('empty frame')
			continue

		if dest_path is not None:
			out_send.write(frame)

	_t = time.time() - _t
	_fps = (_frame_rate*5.) / _t

	print("Harvested {0} frames in {1:04f} seconds.  {2:04f} f.p.s.".format(i+1, _t, _fps))


if __name__ == '__main__':

	_camera_name = "JAI Corporation-WU240330"

	argv = sys.argv[1:]

	if len(argv) == 0:
		do_test(camera=_camera_name, dest_path=None, fps=150)
		sys.exit(1)

	if "-o" in argv:
		do_test(camera=_camera_name, dest_path=argv[1], fps=25)
