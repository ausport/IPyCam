import numpy as np
import cv2
import sys
import os
import time
import getopt
from logger import log, create_file_handler
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

	log.addHandler(create_file_handler('output.log'))

	log.info("Running GStreamer Test:")
	log.info("Device Name:       {0}".format(camera))
	log.info("Target Rate:       {0} f.p.s".format(_frame_rate))
	log.info("Target Resolution: {0}x{1}".format(_width, _height))
	log.info("Capture Duration:  {0} frames.".format(_frame_rate*5))
	log.info("Capture Path:      {0}.".format(dest_path or "n/a"))

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

	log.debug("\t* Harvested {0} frames in {1:04f} seconds.  {2:04f} f.p.s.".format(i+1, _t, _fps))

	log.info("Running OpenCV Tests:")

	# Resize an image
	_t = time.time()
	_tmp = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
	_t = time.time() - _t
	log.debug("\tImage Resize:       {0:02f} msecs".format(_t*1000.))

	# GaussianBlur
	_t = time.time()
	cv2.GaussianBlur(frame,(5,5),0)
	_t = time.time() - _t
	log.debug("\tGaussianBlur:       {0:02f} msecs".format(_t*1000.))

	# Dilation
	_t = time.time()
	kernel = np.ones((5, 5), np.uint8)
	cv2.dilate(frame, kernel, iterations=1)
	_t = time.time() - _t
	log.debug("\tDilation:           {0:02f} msecs".format(_t*1000.))

	# Canny Edge
	_t = time.time()
	cv2.Canny(frame, 100, 200)
	_t = time.time() - _t
	log.debug("\tCanny Edge:         {0:02f} msecs".format(_t*1000.))

	# Fourier Transform
	_t = time.time()
	np.fft.fft2(frame)
	_t = time.time() - _t
	log.debug("\tFourier Transform:  {0:02f} msecs".format(_t*1000.))

	# Hough Transform
	_t = time.time()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 50, 150, apertureSize=3)
	cv2.HoughLines(edges, 1, np.pi / 180, 200)
	_t = time.time() - _t
	log.debug("\tHough Transform:    {0:02f} msecs".format(_t*1000.))


if __name__ == '__main__':

	_camera_name = "JAI Corporation-WU240330"
	print(_camera_name)

	_w = None
	_h = None
	_path = None
	_fps = None

	argumentList = sys.argv[1:]
	unixOptions = "w:h:o:f:"
	gnuOptions = ["width=", "height=", "output=", "fps="]

	try:
		arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
	except getopt.error as err:
		# output error, and return with an error code
		print(str(err))
		sys.exit(2)

	for currentArgument, currentValue in arguments:
		if currentArgument in ("-w", "--width"):
			print("Width = {0}".format(currentValue))
			_w = int(currentValue)
		elif currentArgument in ("-h", "--height"):
			print("Height = {0}".format(currentValue))
			_h = int(currentValue)
		elif currentArgument in ("-f", "--fps"):
			print("FPS = {0}".format(currentValue))
			_fps = int(currentValue)
		elif currentArgument in ("-o", "--output"):
			print("Output = {0}".format(currentValue))
			_path = currentValue

	do_test(camera=_camera_name, dest_path=_path, fps=_fps, w=_w, h=_h)
