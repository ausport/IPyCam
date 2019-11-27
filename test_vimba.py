from pymba import Vimba
from typing import Optional
import cv2
from pymba import Frame
from PIL import Image

# todo add more colours
PIXEL_FORMATS_CONVERSIONS = {
    'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
}


def display_frame(frame: Frame, delay: Optional[int] = 1) -> None:
    """
    Displays the acquired frame.
    :param frame: The frame object to display.
    :param delay: Display delay in milliseconds, use 0 for indefinite.
    """
    print('frame {}'.format(frame.data.frameID))

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

        camera.arm('SingleFrame')

        # capture a single frame, more than once if desired
        for i in range(1):
            try:
                frame = camera.acquire_frame()
                display_frame(frame, 0)
            except:
                pass
                # rearm camera upon frame timeout
                #if e.error_code == VimbaException.ERR_TIMEOUT:
                #    print(e)
                #    camera.disarm()
                #    camera.arm('SingleFrame')
                #else:
                #    raise

        camera.disarm()

        camera.close()
