import io
import math
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

MAX_LUM = 582
MIN_LUM = 182
TARGET_LUM = math.floor(MIN_LUM + (MAX_LUM - MIN_LUM)/2)
ALPHA = 0.25
BOX_HEIGHT = 360
BOX_WIDTH = 640
WEIGHT_MATRIX = np.array([[1 for i in range(640)] for j in range(360)])
NORMALIZATION_FACTOR = 1/(np.max(WEIGHT_MATRIX))

def calculate_avg_box_lum(img):
    flattened_lum = np.add(np.add(image[0],image[1]),image[2])
    

with PiCamera() as camera:
    stream = io.BytesIO()
    camera.resolution = (1920, 1080)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1920,1080))

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        img = np.array(frame.array)
        print(img.shape)
        rawCapture.truncate(0)
        stream.truncate()
        stream.seek(0)
        exit(0)
