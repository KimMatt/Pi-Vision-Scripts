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
WEIGHT_MATRIX = np.array([[1 if i in range (1920/2 - BOX_WIDTH/2, 1920/2 + BOX_WIDTH/2) else 0 for i in range(640)] if j in range(1080/2 - BOX_HEIGHT/2, 1080/2 + BOX_HEIGHT/2) else [0 for i in range(1920)] for j in range(1080)])
NORMALIZATION_FACTOR = 1/(np.max(WEIGHT_MATRIX))

def calculate_avg_box_lum(img):
    flattened_img = np.add(img[0], img[1], img[2])
    weighted_box_lum = np.multiply(WEIGHT_MATRIX,flattened_img)
    return np.sum(weighted_box_lum) / (BOX_WIDTH * BOX_HEIGHT)

with PiCamera() as camera:
    stream = io.BytesIO()
    camera.resolution = (1920, 1080)
    rawCapture = PiRGBArray(camera, size=(1920,1080))

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        img = np.array(frame.array)
        avg_box_lum = calculate_avg_box_lum(img)
        if avg_box_lum > MIN_LUM or avg_box_lum > MAX_LUM:
            exposure_step_size = ALPHA * (TARGET_LUM - avg_box_lum)
            target_exposure = camera.get_current_exposure() + exposure_step_size
            camera.set_exposure(target_exposure)
