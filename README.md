# P(i|y)Camera

PiyCamera is a simple module to use in projects that are run on RaspberryPi SBC as well as conventional PCs. You can use the same functions for your PC webcam and Pi camera

Provides basic camera operations, along with threaded frame reads.
Helpfull when you are developing app on PC and deploying it on Pi.

For some reason when I was writing this I missed that you can use OpenCV with Pi's CSI connected camera by loading one simple module. 
To load this module on Pi use following command:
```sh
$ sudo modprobe bcm2835-v4l2
```
Or add this module into /etc/modules

Pi version of this camera module is not using OpenCV (except for examples), which may be handy. It also uses stream in threaded mode to provide faster framerates than by using OpenCV

Additionally I've added CameraHelper.py to provide simple image operations that I usually use.



### Libraries used

* [OpenCV](https://github.com/opencv/opencv) vision library
* [numpy](https://github.com/numpy/numpy) computing library, providing fast matrices operations
* [PiCamera](https://github.com/waveform80/picamera) standard Pi CSI camera module
