#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 15:25:08 2018

@author: mitchell
"""
from wampImageProc import wampImageProc
import glob
import cv2 
import sys
import time

base_folder = "/home/mitchell/3G-AMP-Calibration"
save_folder = "/home/mitchell/3G-AMP-Calibration/calibration_images"
WIP = wampImageProc(root_dir = base_folder, hour_min = 10, hour_max = 16)
s = 1
for folder in WIP.sub_directories:
    images1 = sorted(glob.glob(folder + 'Manta 1/*.jpg'))
    images2 = sorted(glob.glob(folder + 'Manta 2/*.jpg'))
    images = zip(images1, images2)
    for i, fnames in enumerate(images):
        fname1 = fnames[0]
        
        fname2 = fnames[1]
        
        #print(fname1.split('/')[-1], fname2.split('/')[-1])
        if fname1.split('/')[-1] == fname2.split('/')[-1]:
            img1 = cv2.imread(fname1)
            img2 = cv2.imread(fname2)
            cv2.imshow('img1', img1)
            k = cv2.waitKey(s)
    
            if k == 99:
                cv2.destroyAllWindows()
                sys.exit()
            if k == 10:
                s = 100
                name1 = save_folder + '/img1%s.png' % (i)
                cv2.imwrite(name1, img1) 
                name2 = save_folder + '/img2%s.png' % (i)
                cv2.imwrite(name2, img2) 