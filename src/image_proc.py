#!/usr/bin/env python2.7
"""
Created on Fri Nov  9 15:27:44 2018

Script to process images using the wampImageProc module. Images are processed 
and checked for high overlap values. Uncomment lines 38+ to have data 
saved to disk

@author: mitchell scott
"""
import glob
from wampImageProc import wampImageProc
import os
import sys

if __name__ == '__main__':
    #Determine if to save and what directory to save data to
    save_info = False
    overlap_save = False
    path = None
    if len(sys.argv) == 2:
        save_info = bool(sys.argv[1])
    elif len(sys.argv) == 3:   
        save_info = bool(sys.argv[1])
        overlap_save = bool(sys.argv[2])
    elif len(sys.argv) == 4:
        save_info = bool(sys.argv[1])
        overlap_save = bool(sys.argv[2])
        path = str(sys.argv[3])
    
    if save_info:
        save_directory= path
    elif save_info and path == None:
        save_directory = os.getcwd()
        save_directory = save_directory.split('/')
        save_directory = save_directory[:len(save_directory)-2]
        save_directory = "/".join(save_directory)   
    
    #Find overlap between images
    overlap = []
    ignore_dates = ['/media/WAMP/2018_11_16', '/media/WAMP/2018_11_16'] #something fishy with these files...
    #Location of full WAMP images
    base_folder = "/media/WAMP/*"
    sub_folders = sorted(glob.glob(base_folder))
    #Store high values
    high_value = []
    #Loop through all folders under the root directory
    for folder in sub_folders:
        date = folder.split("/")[3]
        print('Current folder = %s') % (folder)
        #Ignore folders that aren't of specific dates
        if date[0:2] == '20' and folder not in ignore_dates:                   
            #Create a WIP object, initiated with the directory location, only in daylight hours
            WIP = wampImageProc(root_dir = folder, hour_min = 10, hour_max = 16)
            #Check image overlap
            overlap.extend(WIP.image_overlap(display_images = False, only_triggers = True))
            #Check iamges which have high amounts of overlap
            high_value = (WIP.high_overlap_list)
            
            if save_info:
                """
                SAVE DATA FOR IMAGE PROCCESSING
                """
                with open(save_directory + '/high_value.txt', 'a+') as f:
                    for item in high_value:
                        f.write("%s\n" % item)    
    if overlap_save:
        with open(save_directory + '/overlap.txt', 'w+') as f:
            for item in overlap:
                f.write("%s\n" % item)
            