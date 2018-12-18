import cv2
import sys
sys.path.append('../')
from PiyCamera.PiyCamera import OSDetector
if OSDetector.is_embedded():
    from PiyCamera.PiyCamera import PiCamera as PiyCamera
else:
    from PiyCamera.PiyCamera import PyCamera as PiyCamera


if __name__ == '__main__':
    print(OSDetector.is_embedded())
    cam = PiyCamera()   
    cam.get_exposure()
    cam.get_iso()
    cam.get_contrast()
    cam.get_resolution()
    cam.get_brightness()


