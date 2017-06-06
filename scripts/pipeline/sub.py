#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:21:00 2017

@author: noah
"""

from pipeline import *
import numpy as np
import os, subprocess
from astropy.io import fits

def subtract():
    log = getlog()
    output = getoutput()
    recent = getrecent()
    newfolder('subtraction')
    sub_path = getrecent()
    images = getimages(recent)
    for image in images:
        hdulist = fits.open(image)
        template = hdulist[0].header['SDI_TEMP']
        aligned = hdulist[0].header['SDI_ALI']
        hdulist.close()
        if template != 'NA' and aligned == 'Yes':
            template = os.path.join(templates, template)
            out = os.path.join(sub_path, image.split('/')[-1])
            subprocess.call(['hotpants', '-inim', image, '-tmplim', template, '-outim', out])
            hdulist=fits.open(out)
            hdulist[0].header['SDI_SUB'] = 'Yes'
            hdulist.writeto(out, clobber=True)
            hdulist.close()
    updatelog()

    
if __name__ == "__main__":
    subtract()
