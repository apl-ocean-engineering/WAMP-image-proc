#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 08:44:54 2018

Image calibration of SERDP using saved images.

Uses OpenCV Python example code: https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html


@author: mitchell
"""

import numpy as np
import cv2
import glob
import yaml
import numpy as np
from wampImageProc import image_transform

objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
objpoints = [] # 3d point in real world space
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
base_path = '/home/mitchell/3G-AMP-Calibration/calibration_images'
img_shape = (2056, 2464, 3)

def load_intrinsics(load_path):
    mtx = np.array(np.loadtxt(
            load_path + 'intrinsic_matrix.csv', dtype = float, delimiter=','))
    dist = np.array(np.loadtxt(
            load_path + 'distortion_coeffs.csv', dtype = float, delimiter=','))
    
    objpoints_num = np.array(np.loadtxt(
            load_path + 'objpoints_num.csv', dtype = float, delimiter=','))
    
    mtx.reshape((3,3))
    objpoints = []
    for i in range(0, objpoints_num):
        objpoints.append(objp)
    
    return mtx, dist, objpoints
    
def intrinsic_calibration(img_num):
        
    # termination criteria
    
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)

    # Arrays to store object points and image points from all the images.
    imgpoints = [] # 2d points in image plane.
    
    if img_num == 1:
        images = glob.glob(base_path + '/img1*.png')
        save_path = '/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP/camera1/'
    else:
        images = glob.glob(base_path + '/img2*.png')   
        save_path = '/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP/camera2/'
    calc = 0
    for fname in images:
        img = cv2.imread(fname) #Next image 
        print(img.shape)
        cv2.imshow('img', img)
        k = cv2.waitKey(1000)
        if k == 10:   
            #Convert to grayscale for corner detection
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (8,6),None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                calc += 1
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)       
                imgpoints.append(corners2)
                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (8,6), corners2,ret)
                cv2.imshow('img',img)
                cv2.waitKey(5)
                            
                
    objpoints2 = np.array(objpoints)
    objpoints2.reshape((-1))
    """
    calibratecamera(objpoints, imgpoints, imgShape)
    Inputs
        objpoints: identical list of vectors specificying 3D point location
        imgpoints: 2D checkerboard points from corner detection
        imgShape: Image size
    Outputs
        ret: rms error
        mtx: 3X3 camera matrix
        dist: Distortion coefficients [k1, k2, p1, p2, k3]
        rvecs: Output of rotation vectors for each checkerboard view
        tvecs: Output of translational vectors for each checkerboard view
        
    """
    calc = np.array([calc])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, 
                                        imgpoints, gray.shape[::-1], None, None)
    
    np.savetxt(save_path + 'intrinsic_matrix.csv', mtx, fmt='%1.3f', delimiter=",")
    np.savetxt(save_path + 'distortion_coeffs.csv', dist, fmt='%1.3f', delimiter=",")
    np.savetxt(save_path + 'objpoints_num.csv', calc, fmt='%1.3f', delimiter=",")
    
    
    cv2.destroyAllWindows()
    
    return mtx, dist, objpoints

def stereo_calibrate(pnts1, pnts2, intrinsics1, intrinsics2, objpoints):
    mtx1, dist1 = intrinsics1[0], intrinsics1[1]
    print(mtx1, type(mtx1))
    mtx2, dist2 = intrinsics2[0], intrinsics2[1]
    '''
    cv2.stereoCalibrate(
            self.objpoints, self.imgpoints_l,
            self.imgpoints_r, self.M1, self.d1, self.M2, self.d2, dims)
    cv2.stereoCalibrate(obj_points,img_left_points,img_right_points,image_size,criteria = stereocalib_criteria, flags = stereocalib_flags)
    '''
    stereo_calibration = cv2.stereoCalibrate(objpoints, pnts1, pnts2, img_shape)

if __name__ == '__main__':
    #intrinsics1 = intrinsic_calibration(1)
    #intrinsics2 = intrinsic_calibration(2)
    intrinsics1 = load_intrinsics('/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP/camera1/')
    intrinsics2 = load_intrinsics('/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP/camera2/')
    
    CP = image_transform(base_path)
    CP.corresponding_image_points()
    pnts1, pnts2 = CP.get_points()
    
    stereo_calibrate(pnts1, pnts2, intrinsics1, intrinsics2, intrinsics1[2])
    

