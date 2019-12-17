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
	print("\tDevice Name:       {0}".format(camera))
	print("\tTarget Rate:       {0} f.p.s".format(_frame_rate))
	print("\tTarget Resolution: {0}x{1}".format(_width, _height))
	print("\tCapture Duration:  {0} frames.".format(_frame_rate*5))
	print("\tCapture Path:      {0}.".format(dest_path or "n/a"))


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

	print("\n\t* Harvested {0} frames in {1:04f} seconds.  {2:04f} f.p.s.".format(i+1, _t, _fps))

	print("\n* * * * * * * * * *")
	print("Running OpenCV Tests:")

	# Resize an image
	_t = time.time()
	_tmp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
	_t = time.time() - _t
	print("\tImage Resize:       {0:02f} msecs".format(_t*1000.))

	# GaussianBlur
	_t = time.time()
	cv2.GaussianBlur(frame,(5,5),0)
	_t = time.time() - _t
	print("\tGaussianBlur:       {0:02f} msecs".format(_t*1000.))

	# Dilation
	_t = time.time()
	kernel = np.ones((5, 5), np.uint8)
	cv2.dilate(frame, kernel, iterations=1)
	_t = time.time() - _t
	print("\tDilation:           {0:02f} msecs".format(_t*1000.))

	# Canny Edge
	_t = time.time()
	cv2.Canny(frame, 100, 200)
	_t = time.time() - _t
	print("\tCanny Edge:         {0:02f} msecs".format(_t*1000.))

	# Fourier Transform
	_t = time.time()
	np.fft.fft2(frame)
	_t = time.time() - _t
	print("\tFourier Transform:  {0:02f} msecs".format(_t*1000.))

	# Hough Transform
	_t = time.time()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 50, 150, apertureSize=3)
	cv2.HoughLines(edges, 1, np.pi / 180, 200)
	_t = time.time() - _t
	print("\tHough Transform:    {0:02f} msecs".format(_t*1000.))
	print("* * * * * * * * * *")

	# TODO - Long results in log file.

if __name__ == '__main__':

	_camera_name = "JAI Corporation-WU240330"

	argv = sys.argv[1:]

	if len(argv) == 0:
		do_test(camera=_camera_name, dest_path=None, fps=150, w=600, h=600)
		sys.exit(1)

	if "-o" in argv:
		do_test(camera=_camera_name, dest_path=argv[1], fps=25)
