#!/usr/bin/env python2.7
"""
Created on Fri Nov  9 15:27:44 2018

@author: mitchell
"""

from wampImageProc import wampImageProc, image_transform

if __name__ == '__main__':
    """
    Determine affine transformation
    PMC = image_transform("/home/mitchell/WAMP_workspace/2018_10_29 13_09_47")
    PMC.corresponding_image_points()
    print(PMC.find_affine(save=True))
    """
    #Specify folder lcoation wit base image directory
    folder_location = "/home/mitchell/WAMP_workspace"
    
    #Create a WIP object, initiated with the directory location
    WIP = wampImageProc(root_dir = folder_location, hour_min = 10, hour_max = 16)
    
    #Call Video Peak Source (void). Will display combined image
    overlap_intensity = WIP.image_overlap(display_overlap = True)
    
    