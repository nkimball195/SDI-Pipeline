#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:19:19 2017

@author: noah
"""
from pipeline import *
import numpy as np
import os, subprocess
from astropy.io import fits

def align():
    log = getlog()
    output = getoutput()
    recent = getrecent()    
    newfolder('aligned')
    ali_path = getrecent()    
    images = getimages(recent)
    for image in images:
        hdulist = fits.open(image)
        template = hdulist[0].header['SDI_TEMP']
        hdulist.close()
        if template != 'NA':
            template = os.path.join(templates, template)
            out = os.path.join(ali_path, image.split('/')[-1])
            subprocess.call(['wcsremap', '-template', template, '-source', image, '-outIm', out])
            hdulist=fits.open(out)
            hdulist[0].header['SDI_ALI'] = 'Yes'
            hdulist.writeto(out, clobber=True)
            hdulist.close()
    updatelog()
    
if __name__ == "__main__":
    align()
