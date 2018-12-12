#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 09:41:47 2018

@author: mitchell
"""
import logging
import argparse
from os.path import dirname, abspath

parser = argparse.ArgumentParser(description='Save generated camera info')
parser.add_argument('--save_trigger_data', default = 'False',
                    help = 'Set to True to save trigger data to data folder')
parser.add_argument('--save_overlap_data', default = 'False',
                    help = 'Set to True to save trigger data to data folder')

parent_directory = dirname(dirname(abspath(__file__)))

args = parser.parse_args()
print(bool(args.save_overlap_data))