#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 09:29:25 2018

@author: mitchell
"""

from wampImageProc import wampImageProc

if __name__ == '__main__':
    #Load high value data
    high_events = []
    with open('/home/mitchell/WAMP_workspace/high_value.txt', 'r') as f:
        for line in f:
            high_events.append(line)
    #View all high value events
    viewed_events = set()
    for event in high_events:
        WIP = wampImageProc(root_dir = '/media/WAMP/' + event.split(' ')[0])
        triggered_events = WIP.trigger_dates
        #print(triggered_events)
        
        if event.split(' ')[0] not in viewed_events:# and event.replace(' ', '_').strip('\n') in triggered_events:
            print(event)
            WIP.single_directiory_background_subtraction(event)
            viewed_events.add(event.split(' ')[0])
                