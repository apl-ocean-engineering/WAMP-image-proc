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
import matplotlib.pyplot as plt

objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
objpoints = [] # 3d point in real world space
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
base_path = '/home/mitchell/3G-AMP-Calibration/calibration_images'
base_save_path = '/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP'
stereo_save_path = '/home/mitchell/WAMP_workspace/WAMP-image-proc/calibration/3G-AMP'
img_shape = (2056, 2464)




def drawlines(img1,img2,lines,pts1,pts2, num):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c = (2056, 2464)
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        #print(r, pt1, pt2)
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        name = 'img%s' % (num)
        cv2.imshow(name, img1)
        k = cv2.waitKey(0)
        point1 = (pt1[0][0], pt1[0][1])
        point2 = (pt2[0][0], pt2[0][1])
        img1 = cv2.circle(img1, point1,5,color,-1)
        img2 = cv2.circle(img2, point2,5,color,-1)
    return img1,img2

def calibration():
    """
    Intrinsic
    """
    cv2.namedWindow('img1', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img1', 800,800)
    cv2.namedWindow('img2', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('img2', 800,800)
    imgpoints1 = [] # 2d points in image plane.
    imgpoints2 = []
    i = 0
    imgs1 = sorted(glob.glob(base_path + '/img1*.png'))
    save_path1 = base_save_path + '/camera1/'
    imgs2 = sorted(glob.glob(base_path + '/img2*.png'))
    save_path2 = base_save_path + '/camera1/'
    
    images = zip(imgs1, imgs2)
    
    for fname1, fname2 in images:
        i += 1
        img1 = cv2.imread(fname1) #Next image 
        img2 = cv2.imread(fname2)
        cv2.imshow('img1', img1)
        cv2.imshow('img2', img2)
        if i == 1:
            cv2.waitKey(2000)
        k = cv2.waitKey(1000)
        
        if k == 10:   
            #Convert to grayscale for corner detection
            gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
            img1s = gray1
            img2s = gray2
            # Find the chess board corners
            ret1, corners_cam1 = cv2.findChessboardCorners(gray1, (8,6), None)
            ret2, corners_cam2 = cv2.findChessboardCorners(gray2, (8,6), None)
            
            if ret1 and ret2:
                objpoints.append(objp)
                corners_cam1_2 = cv2.cornerSubPix(gray1,corners_cam1,(11,11),(-1,-1),criteria)       
                corners_cam2_2 = cv2.cornerSubPix(gray1,corners_cam2,(11,11),(-1,-1),criteria) 
                
                imgpoints1.append(corners_cam1_2)
                imgpoints2.append(corners_cam2_2)
                # Draw and display the corners
                img1 = cv2.drawChessboardCorners(img1, (8,6), corners_cam1_2,ret1)
                img2 = cv2.drawChessboardCorners(img2, (8,6), corners_cam2_2,ret2)
                cv2.imshow('img1',img1)
                cv2.imshow('img2',img2)
                cv2.waitKey(5)          
                
    ret1, mtx1, dist1, rvecs1, tvecs1 = cv2.calibrateCamera(objpoints, 
                                        imgpoints1, gray1.shape[::-1], None, None)
    
    np.savetxt(save_path1 + 'intrinsic_matrix.csv', mtx1, fmt='%1.3f', delimiter=",")
    np.savetxt(save_path1 + 'distortion_coeffs.csv', dist1, fmt='%1.3f', delimiter=",")   
    
    ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(objpoints, 
                                        imgpoints2, gray2.shape[::-1], None, None)
    
    np.savetxt(save_path2 + 'intrinsic_matrix.csv', mtx2, fmt='%1.3f', delimiter=",")
    np.savetxt(save_path2 + 'distortion_coeffs.csv', dist2, fmt='%1.3f', delimiter=",")      
    
    """
    Stereo
    v2.stereoCalibrate(objectPoints, imagePoints1, imagePoints2, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize[, R[, T[, E[, F[, flags[, criteria]]]]]])
    """
    #print('IMGPOINTS1')
    #print(imgpoints1)
    #print('IMGPOINTS2')
    #print(imgpoints2)    
    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, img_shape, criteria = criteria, flags=cv2.CALIB_FIX_INTRINSIC)
    print('R', R)
    print('T', T)
    print('E', E)
    print('F', F)
    
    np.savetxt(stereo_save_path + '/rotation_matrix.csv', R, fmt='%1.3f', delimiter=",")
    np.savetxt(stereo_save_path + '/translation_matrix.csv', T, fmt='%1.3f', delimiter=",")
    np.savetxt(stereo_save_path + '/essential_matrix.csv', E, fmt='%1.3f', delimiter=",")
    np.savetxt(stereo_save_path + '/fundemental_matrix.csv', F, fmt='%1.3f', delimiter=",")
    
    # Find epilines corresponding to points in right image (second image) and
    # drawing its lines on left image
    imgpoints1 = np.asarray(imgpoints1)[0]
    #print(imgpoints1, type(imgpoints1), len(imgpoints1))
    imgpoints2 = np.asarray(imgpoints2)[0]
    lines1 = cv2.computeCorrespondEpilines(imgpoints2.reshape(-1,1,2), 2,F)
    lines1 = lines1.reshape(-1,3)
    img5,img6 = drawlines(img1s,img2s,lines1,imgpoints1,imgpoints2, 1)
    
    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv2.computeCorrespondEpilines(imgpoints1.reshape(-1,1,2), 1,F)
    lines2 = lines2.reshape(-1,3)
    img3,img4 = drawlines(img2s,img1s,lines2,imgpoints2,imgpoints1, 2)
    
    plt.subplot(121),plt.imshow(img5)
    plt.subplot(122),plt.imshow(img3)
    plt.show()
    
    cv2.destroyAllWindows()   

if __name__ == '__main__':
    calibration()        