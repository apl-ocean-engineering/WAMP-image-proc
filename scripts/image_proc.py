#!/usr/bin/env python2.7
"""
Created on Fri Nov  9 15:27:44 2018

Script to process images using the wampImageProc module. Images are processed 
and checked for high overlap values. Uncomment lines 38+ to have data 
saved to disk

@author: mitchell scott
"""
import logging
import logging.handlers
import argparse
import os
from os.path import dirname, abspath
import glob
from wampImageProc import wampImageProc

#Setup logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#Parse inputs
parser = argparse.ArgumentParser(description='Save generated camera info')
parser.add_argument('--save_trigger_data', default = 'False',
            help = 'Set to True to save stereo triggers data to data folder')
parser.add_argument('--save_overlap_data', default = 'False',
            help = 'Set to True to save overlap data to data folder')

args = parser.parse_args()
save_triggers = bool(args.save_trigger_data)
save_overlap = bool(args.save_overlap_data)
print(save_triggers, save_overlap)

save_directory = dirname(dirname(abspath(__file__))) #/<path_to_workspace>/data

"""
Loop through all folders under the base_folder, check images from high levels 
of overlap. Optinal: save overlap and high trigger data to /data folder
"""
#Find overlap between images
#overlap = []
#TODO: Something is fishy (hehe) with these files? Ignore them for now...
ignore_dates = ['/media/WAMP/2018_11_16', '/media/WAMP/2018_11_16', '/media/WAMP/2018_12_05']
#Location of full WAMP images
base_folder = "/media/WAMP/*"
sub_folders = sorted(glob.glob(base_folder))
#Store high values
high_value = []
#Loop through all folders under the root directory
for folder in sub_folders:
    current_folder = 'Current folder: %s' % (str(folder))
    logging.info(current_folder)
    date = folder.split("/")[3]
    #Ignore folders that aren't of specific dates
    if date[0:2] == '20' and folder not in ignore_dates:    
        month = int(date.split('_')[1])
        day = int(date.split('_')[2])
        #Only search over daylight hours
        WIP = wampImageProc(root_dir = folder, hour_min = 10, hour_max = 16)
        #Check image overlap
        overlap = WIP.image_overlap(display_images = False, 
                                         only_triggers = True)
        #Check iamges which have high amounts of overlap
        high_value = (WIP.high_overlap_list)
        '''
        OPTIONAL: Save data
        '''
        
        
        if save_triggers:
            path = save_directory + '/data/%s' % str(WIP.high_overlap)
            if not os.path.exists(path):
                os.makedirs(path)
            name = save_directory + '/data/%s/triggers.txt' % str(WIP.high_overlap)
            with open(name, 'a+') as f:
                for item in high_value:
                    f.write("%s\n" % item)   
            logger.debug("Wrote Triggers to folder")
        if save_overlap:
            path = save_directory + '/data/%s' % str(WIP.high_overlap)
            if not os.path.exists(path):
                os.makedirs(path)
            name = save_directory + '/data/%s/overlap.txt' % str(WIP.high_overlap)
            with open(name, 'w+') as f:
                for item in overlap:
                    f.write("%s\n" % item)
            logger.debug("Wrote Overlap to folder")
                
            