import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
from wampImageProc import calibration
from types import FunctionType

C = calibration()

image_path = '/home/mitchell/3G-AMP-Calibration/calibration_images'
base_save_path = '/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP'

#a = [x for x, y in C.__dict__.items() if type(y) == FunctionType]
#print(C.__dict__.items())


C.stereo_calibrate(image_path + '/Manta 1/2018_12_12_14_19_57.52.jpg', 
                        image_path + '/Manta 2/2018_12_12_14_19_57.52.jpg', save = True, intrinsics_load_path = base_save_path, stereo_save_path = base_save_path)
