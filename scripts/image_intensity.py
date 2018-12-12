#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 16:47:30 2018

@author: mitchell
"""

from wampImageProc import wampImageProc

if __name__ == '__main__':
    
    folder_location = "/media/WAMP/2018_10_16"
    WIP = wampImageProc(root_dir = folder_location, hour_min = 10, hour_max = 16)
    overlap_intensity = WIP.image_overlap(display_overlap = False)