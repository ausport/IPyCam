from pymba import Vimba, Frame
from typing import Optional
import cv2
from PIL import Image
from time import sleep

# todo add more colours
PIXEL_FORMATS_CONVERSIONS = {
    'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
}

_frames = []

def display_frame(frame: Frame, delay: Optional[int] = 1) -> None:
    """
    Displays the acquired frame.
    :param frame: The frame object to display.
    :param delay: Display delay in milliseconds, use 0 for indefinite.
    """
    print('frame {}'.format(frame.data.frameID))
    _frames.append(frame)
    return
    
    # get a copy of the frame data
    image = frame.buffer_data_numpy()

    # convert colour space if desired
    try:
        image = cv2.cvtColor(image, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
    except KeyError:
        pass

    # display image
    # cv2.imshow('Image', image)
    # cv2.waitKey(delay)
    print(image.__class__.__name__)
    # _path = "https://www.dropbox.com/request/GDRwtJglQhY2sHn9VPh5/test.png"
    im = Image.fromarray(image)
    
    im.save("./image.png")



if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # arm the camera and provide a function to be called upon frame ready
        camera.arm('Continuous', display_frame)
        camera.start_frame_acquisition()

        sleep(5)

        # stop frame acquisition
        # start_frame_acquisition can simply be called again if the camera is still armed
        camera.stop_frame_acquisition()
        camera.disarm()

        camera.close()
