import cv2
import sys
sys.path.append('../')
from PiyCamera.PiyCamera import OSDetector
if OSDetector.is_embedded():
    from PiyCamera.PiyCamera import PiCamera as PiyCamera
else:
    from PiyCamera.PiyCamera import PyCamera as PiyCamera
from PiyCamera.CameraHelper import ImageOperations


if __name__ == '__main__':

    cam = PiyCamera()
    cam.start_camera_thread()
    cam.set_resolution(1920, 1080)

    while True:
        image = cam.read_frame()
        image = ImageOperations.flip_vertical(image)
        if image is not None:
            cv2.imshow('img', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break