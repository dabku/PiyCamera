from threading import Thread
import logging
logger = logging.getLogger(__name__)

class OSDetector:
    @staticmethod
    def is_windows():
        import os
        if os.name == 'nt':
            return True
        return False

    @staticmethod
    def is_embedded():
        import os
        try:
            if 'arm' in os.uname()[-1]:
                return True
        except AttributeError:
            pass
        return False

class PiyCamera:
    def __init__(self):
        self._camera_thread = None
        self._run = False
        self._frame = None
        self._video_capture = None

    def get_frame(self):
        raise NotImplementedError

    def read_frame(self):
        raise NotImplementedError

    def update_frame(self):
        raise NotImplementedError

    def start_camera_thread(self):
        self._run = True
        self._camera_thread = Thread(target=self.camera_worker)
        self._camera_thread.setDaemon(True)
        self._camera_thread.start()

    def stop_camera_thread(self):
        self._run = False
        self._camera_thread.join()

    def camera_worker(self):
        raise NotImplementedError

    def save_image(self):
        raise NotImplementedError

    def set_resolution(self, width, height):
        raise NotImplementedError

    def get_resolution(self):
        raise NotImplementedError

    def set_iso(self, iso):
        raise NotImplementedError

    def get_iso(self):
        raise NotImplementedError

    def set_fps(self, fps):
        raise NotImplementedError

    def get_fps(self):
        raise NotImplementedError

    def set_brightness(self, brightness):
        raise NotImplementedError

    def get_brightness(self):
        raise NotImplementedError

    def set_contrast(self, contrast):
        raise NotImplementedError

    def get_contrast(self):
        raise NotImplementedError

    def set_exposure(self, exposure):
        raise NotImplementedError

    def get_exposure(self):
        raise NotImplementedError

#    def set_shutter_speed(self, speed):
#        raise NotImplementedError

#    def get_shutter_speed(self):
 #       raise NotImplementedError

    def get_settings(self):
        return {'iso': self.get_iso(),
                'resolution': self.get_resolution(),
                'fps': self.get_fps(),
                'brightness': self.get_brightness(),
                'exposure': self.get_exposure(),
                'contrast': self.get_contrast()
        }

def change_settings(func):
    def func_wrapper(self, *args):
        if self._run:
            logging.debug('Stopping camera worker to apply new settings..')
            self.stop_camera_thread()
            func(self, *args)
            logging.debug('Restarting camera worker after settings change')
            self.start_camera_thread()
        else:
            func(self, *args)

    return func_wrapper


class PyCamera(PiyCamera):
    def __init__(self, device_no=0):
        global imwrite
        from cv2 import VideoCapture, imwrite
        import cv2
        super(PyCamera, self).__init__()
        self._video_capture = VideoCapture(device_no)
        self._validate_module()

    @staticmethod
    def _validate_module():
        if OSDetector.is_embedded():
            from subprocess import call
            response = call(['lsmod | grep bcm...._v4l2'], shell=True)
            if len(response) <= 1:
                logger.warning('It seems you are trying to use OpenCV camera on RaspberryPi. '
                           'Make sure that v4l2 module is loaded as it was not detected')

    def get_frame(self):
        return self._frame

    def read_frame(self):
        if self._camera_thread is None:
            for i in range(5):
                self._video_capture.grab()
        self.update_frame()
        return self.get_frame()

    def update_frame(self):
        got_frame = False
        while not got_frame:
            got_frame, frame = self._video_capture.read()
        self._frame = frame

    def camera_worker(self):
        while self._run:
            logger.info('frame')
            self._video_capture.grab()

    def save_image(self, img_path):
        status = imwrite(img_path, self._frame)
        return status

    @change_settings
    def set_resolution(self, width=1280, height=1024):
        self._video_capture.set(3, width)
        self._video_capture.set(4, height)

    def get_resolution(self):
        return int(self._video_capture.get(3)), int(self._video_capture.get(4))

    @change_settings
    def set_brightness(self, brightness):
        self._video_capture.set(10,brightness)

    def get_brightness(self):
        return self._video_capture.get(10)

    @change_settings
    def set_contrast(self, contrast):
        self._video_capture.set(11, contrast)

    def get_contrast(self):
        return self._video_capture.get(11)

    @change_settings
    def set_exposure(self, exposure):
        self._video_capture.set(15,exposure)

    def get_exposure(self):
        return self._video_capture.get(15)

    @change_settings
    def set_fps(self, fps):
        self._video_capture.set(5,fps)

    def get_fps(self):
        return self._video_capture.get(5)

    @change_settings
    def set_iso(self, iso):
        logger.warning('Opencv does not support ISO setting')

    def get_iso(self):
        logger.warning('Opencv does not support ISO setting')
        return -1


class PiCamera(PiyCamera):
    def __init__(self):
        from picamera import PiCamera as PiCam
        from picamera.array import PiRGBArray
        super(PiCamera, self).__init__()
        self._video_capture = PiCam()
        self._raw_capture = PiRGBArray(self._video_capture)

        self.stream = None
        
    def get_frame(self):
        return self._frame

    def read_frame(self):
        if not self._run:
            self.update_frame()
        return self.get_frame()

    def update_frame(self):
        self._raw_capture.truncate(0)
        self._video_capture.capture(self._raw_capture, format="bgr")
        self._frame = self._raw_capture.array

    def camera_worker(self):
        self.stream = self._video_capture .capture_continuous(self._raw_capture,
                                                              format="bgr", use_video_port=True)
        logger.debug('Camera worker started...')
        for f in self.stream:
            self._frame = f.array
            self._raw_capture.truncate(0)
            if not self._run:
                self.stream.close()
                
        logger.debug('Camera worker ended...')

    @change_settings
    def set_resolution(self, width=1024, height=768):
        from picamera.array import PiRGBArray
        self._video_capture.resolution = (width, height)
        self._raw_capture = PiRGBArray(self._video_capture)
       
    def get_resolution(self):
        raise NotImplementedError

    def set_brightness(self, brightness=50):
        if brightness<0:
            brightness = 0
        elif brightness > 100:
            brightness = 100
        self._video_capture.brightness = brightness

    def get_brightness(self):
        return self._video_capture.brightness

    def set_contrast(self, contrast=0):
        if contrast < -100:
            contrast = -100
        elif contrast > 100:
            contrast = 100
        self._video_capture.contrast = contrast

    def get_contrast(self):
        return self._video_capture.contrast

    def set_exposure(self, exposure=0):
        if exposure < -25:
            exposure = -25
        elif exposure > 25:
            exposure = 25
        self._video_capture.exposure_compenstation = exposure

    def get_exposure(self):
        return self._video_capture.exposure_compenstation

    def set_fps(self, fps):
        raise NotImplementedError

    def get_fps(self):
        return self._video_capture.framerate

    def set_iso(self, iso=0):
        if iso < 0:
            iso = 0
        elif iso > 800:
            iso = 800
        self._video_capture.iso = iso

    def get_iso(self):
        return self._video_capture.iso = iso


