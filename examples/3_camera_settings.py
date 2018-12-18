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
    print('Exposure: {}'.format(cam.get_exposure()))
    print('ISO: {}'.format(cam.get_iso()))
    print('Contrast: {}'.format(cam.get_contrast()))
    print('Resolution: {}'.format(cam.get_resolution()))
    print('Brightness: {}'.format(cam.get_brightness()))


