#!/usr/bin/env python2.7
"""
Created on Fri Nov  9 15:27:44 2018

@author: mitchell
"""
import numpy as np
import glob
from wampImageProc import wampImageProc, image_transform

if __name__ == '__main__':
    """
    Determine affine transformation
    PMC = image_transform("/home/mitchell/WAMP_workspace/2018_10_29 13_09_47")
    PMC.corresponding_image_points()
    print(PMC.find_affine(save=True))
    """
    overlap_intensity = []
    previous_dates = ['/media/WAMP/2018_11_18']
    base_folder = "/media/WAMP/*"
    sub_folders = sorted(glob.glob(base_folder))
    high_value = []
    for folder in sub_folders:
        date = folder.split("/")[3]
        if date[0:2] == '20' and folder not in previous_dates:
            print(folder)
            #Specify folder lcoation wit base image directory            
            #Create a WIP object, initiated with the directory location
            WIP = wampImageProc(root_dir = folder, hour_min = 10, hour_max = 16)
            overlap_intensity.extend(WIP.image_overlap(display_images = False, only_triggers = True))
            high_value = (WIP.high_overlap_list)
        
            with open('/home/mitchell/WAMP_workspace/high_value.txt', 'a+') as f:
                for item in high_value:
                    f.write("%s\n" % item)    
    