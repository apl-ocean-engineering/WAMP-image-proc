#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 13:40:16 2018

@author: mitchell
"""
from wampImageProc import image_transform
if __name__ == '__main__':
    """
    Determine affine transformation
    """
    PMC = image_transform("/media/WAMP/2018_11_22/2018_11_22 12_26_42")
    PMC.corresponding_image_points()
    PMC.find_affine(save=True)
    