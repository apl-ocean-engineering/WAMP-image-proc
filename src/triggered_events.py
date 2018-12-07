#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 09:29:25 2018

Analyze triggered events. Assumes there is a file called 'high_value.txt'
which will point to folders which were both triggered and had high overlap values

@author: mitchell scott
"""
from wampImageProc import wampImageProc
import os

if __name__ == '__main__':
    #Determine main directory to save data to
    open_directory = os.getcwd()
    open_directory = open_directory.split('/')
    open_directory = open_directory[:len(open_directory)-2]
    open_directory = "/".join(open_directory)  
    
    #Load high value data
    high_events = []
    with open(open_directory + '/high_value.txt', 'r') as f:
        for line in f:
            high_events.append(line)
    
    #View all high value events
    viewed_events = set()
    for event in high_events:
        WIP = wampImageProc(root_dir = '/media/WAMP/' + event.split(' ')[0])
        #Determine which events were triggered
        triggered_events = WIP.trigger_dates
        
        #If we haven't already looked at these events, display
        if event.split(' ')[0] not in viewed_events:
            WIP.single_directiory_background_subtraction(event)
            viewed_events.add(event.split(' ')[0])
    
                