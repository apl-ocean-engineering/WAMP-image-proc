#!/usr/bin/env python2.7
"""
Created on Wed Nov 14 16:07:34 2018

@author: Mitchell Scott
@contact: miscott@uw.edu
"""
from wampImageProc import calibration

if __name__ == '__main__':
    image_path = '/home/mitchell/3G-AMP-Calibration/calibration_images'
    base_save_path = '/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP'
    
    C = calibration()
    C.intrinsic_calibration(intrinsic_images_path = image_path)
    '''
    Stereo calibration
    '''
    C.stereo_calibrate(image_path + '/Manta 1/2018_12_12_14_19_57.52.jpg', 
                            image_path + '/Manta 2/2018_12_12_14_19_57.52.jpg', 
                            save = True, intrinsics_load_path = base_save_path, 
                            stereo_save_path = base_save_path)
