from pymba import Vimba, Frame
from typing import Optional
import cv2
from PIL import Image
import getopt, sys
from time import sleep

# todo add more colours
PIXEL_FORMATS_CONVERSIONS = {
    'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
}

_frames = []


def log_camera_props(camera):

    feature = camera.feature("DeviceVendorName")
    print("Found camera device:\n* * * * * * * * * * * *\nDeviceVendorName: {0}".format(feature.value))

    feature = camera.feature("DeviceModelName")
    print("DeviceModelName: {0}".format(feature.value))
    print(feature.info)

    feature = camera.feature("PixelFormat")
    print("PixelFormat: {0}".format(feature.value))

    feature = camera.feature("Width")
    print("Default Width: {0}".format(feature.value))

    feature = camera.feature("Height")
    print("Default Height: {0}".format(feature.value))

    feature = camera.feature("WidthMax")
    print("WidthMax: {0}".format(feature.value))

    feature = camera.feature("HeightMax")
    print("HeightMax: {0}".format(feature.value))

    feature = camera.feature("AcquisitionMode")
    print("AcquisitionMode: {0}\n* * * * * * * * * * * *".format(feature.value))

    # for feature_name in camera.feature_names():
    #     print(feature_name)

def display_frame(frame: Frame, delay: Optional[int] = 1) -> None:
    """
    Displays the acquired frame.
    :param frame: The frame object to display.
    :param delay: Display delay in milliseconds, use 0 for indefinite.
    """
    # print('frame {}'.format(frame.data.frameID))
    
    # get a copy of the frame data
    _frames.append(frame)

def main():
    # print command line arguments

    _resolution = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        sys.exit(2)

    for o, a in opts:
        if o == "-r":
            print("Setting resolution to {0}x{0}".format(a))
            _resolution = a

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # Max values
        feature = camera.feature("WidthMax")
        _w = feature.value
        feature = camera.feature("HeightMax")
        _h = feature.value

        if _resolution is not None:
            _w = _resolution
            _h = _resolution

        feature = camera.feature("Width")
        feature.value = int(_w)
        feature = camera.feature("Height")
        feature.value = int(_h)

        log_camera_props(camera)

        # arm the camera and provide a function to be called upon frame ready
        camera.arm('Continuous', display_frame)

        camera.start_frame_acquisition()

        sleep(3.)

        print("Harvested {0} in 3.0 seconds.  {1} f.p.s.".format(len(_frames), float(len(_frames))/3.))

        # stop frame acquisition
        # start_frame_acquisition can simply be called again if the camera is still armed
        camera.stop_frame_acquisition()
        camera.disarm()

        camera.close()

        sys.exit(1)

        for frame in _frames:
            print(frame.data.frameID)
            # get a copy of the frame data
            image = frame.buffer_data_numpy()

            # convert colour space if desired
            try:
                image = cv2.cvtColor(image, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
            except KeyError:
                pass

            continue

            im = Image.fromarray(image)
            im.save("./image{0}.png".format(frame.data.frameID))


if __name__ == '__main__':
    main()



