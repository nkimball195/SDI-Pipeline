#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:24:10 2017

@author: noah
"""

import pyfits
import numpy as np
import os
from pipeline import *

def maketemplate(name):
    #Decompress files and images
    zips=0
    for root, dirs, files in os.walk(input):
        for file in files:
            if file.endswith('.zip'):
                zips=os.path.join(root, file)
                os.system('unzip %s -d %s' % (zips, input))
                zips=1
    for root, dirs, files in os.walk(input):
        for file in files:
            if file.endswith('.fz'):
                fz=os.path.join(root, file)
                os.system('funpack %s' % fz)
                os.system('rm %s' % fz)
    
    #Importing input images and creating list
    images=getimages(input)
    images.sort()
    for image in images:
        hdulist = pyfits.open(images[0])
        temphdu=hdulist[0]
        tempfilter=hdulist[0].header['FILTER']
        tempRA=hdulist[0].header['CAT-RA']
        tempDEC=hdulist[0].header['CAT-DEC']
        temphdu.header['SDI_NAME'] = '%s' % image.split('/')[-1]
        temphdu.header['SDI_TEMP'] = 'NA'
        hdulist.writeto('%s' % images[0], clobber=True)
        hdulist.close()
        hdulist = pyfits.open(image)
        imagehdu=hdulist[0]
        imagefilter=hdulist[0].header['FILTER']
        imageRA=hdulist[0].header['CAT-RA']
        imageDEC=hdulist[0].header['CAT-DEC']
        imagehdu.header['SDI_NAME'] = '%s' % image.split('/')[-1]
        imagehdu.header['SDI_TEMP'] = 'NA'
        hdulist.writeto('%s' % image, clobber=True)
        hdulist.close()