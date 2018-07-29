import numpy as np
from cv2 import imencode, resize

class OsDetector:
    @staticmethod
    def is_windows():
        import os
        if os.name == 'nt':
            return True
        return False
    @staticmethod
    def is_embeeded():
        import os
        try:
            if 'arm' in os.uname[-1]:
                return True
        except AttributeError:
            pass
        return False


def create_blank_image_w(height=480, width=640):
    return np.zeros((width, height, 3), np.uint8)+255


def create_blank_image_b(height=480, width=640):
    return np.zeros((width, height, 3), np.uint8)


def get_jpg_from_frame(frame):
    return imencode('.jpg', frame)[1].tobytes()


def get_png_from_frame(frame):
    return imencode('.png', frame)[1].tobytes()


def flip_vertical(frame):
    return np.fliplr(frame)


def flip_horizontal(frame):
    return np.flipud(frame)


def flip_both(frame):
    return np.fliplr(np.flipud(frame))


def get_frame_mean(frame):
    return np.mean(frame)

def resize_image(frame, width, height):
    return resize(frame, (width, height))


