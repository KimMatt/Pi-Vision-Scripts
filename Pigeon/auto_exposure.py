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
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
WEIGHT_MATRIX = np.array([[1 if i in range (int(CAMERA_WIDTH/2 - BOX_WIDTH/2), int(CAMERA_WIDTH/2 + BOX_WIDTH/2)) else 0 for i in range(CAMERA_WIDTH)] if j in range(int(CAMERA_HEIGHT/2 - BOX_HEIGHT/2), int(CAMERA_HEIGHT/2 + BOX_HEIGHT/2)) else [0 for i in range(CAMERA_WIDTH)] for j in range(CAMERA_HEIGHT)])
NORMALIZATION_FACTOR = 1/(np.max(np.max(WEIGHT_MATRIX)))

def calculate_avg_box_lum(img):
    print(img.shape)
    print(img[:][0][:].shape) 
    flattened_img = np.add(np.add(img[:,:,0], img[:,:,1]), img[:,:,2])
    print(WEIGHT_MATRIX.shape, flattened_img.shape)  
    weighted_box_lum = np.multiply(WEIGHT_MATRIX,flattened_img)
    return np.sum(weighted_box_lum) / (BOX_WIDTH * BOX_HEIGHT)

with PiCamera() as camera:
    #stream = io.BytesIO()
    camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
    rawCapture = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))

    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        img = np.array(frame.array)
        avg_box_lum = calculate_avg_box_lum(img)
        if avg_box_lum > MIN_LUM or avg_box_lum > MAX_LUM:
            exposure_step_size = ALPHA * (TARGET_LUM - avg_box_lum)
            target_exposure = camera.get_current_exposure() + exposure_step_size
            #rawCapture.truncate(0)
            camera.set_exposure(target_exposure)
            print("target exposure: " + str(target_exposure)) 
            rawCapture.truncate(0)
            rawCapture.seek(0)
