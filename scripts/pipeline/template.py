#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:24:10 2017

@author: noah
"""

import pyfits
import numpy as np
import os, subprocess
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

    stack = []
    images=getimages(input)
    images.sort()
    template = images[0]
    hdulist = pyfits.open(template)
    tempfilter=hdulist[0].header['FILTER']
    tempRA=hdulist[0].header['CAT-RA']
    tempDEC=hdulist[0].header['CAT-DEC']
    hdulist.close()
    for image in images:
        hdulist = pyfits.open(image)
        imagefilter=hdulist[0].header['FILTER']
        imageRA=hdulist[0].header['CAT-RA']
        imageDEC=hdulist[0].header['CAT-DEC']
        hdulist.close()
        if tempRA==imageRA and tempDEC==imageDEC and tempfilter==imagefilter:
            out = image.split('.fits')[0] + '_rm.fits'
            subprocess.call(['wcsremap', '-template', template, '-source', image, '-outIm', out])
            stack.append(pyfits.open(image)[0].data.copy())
    stack = np.median(np.array(stack),0)
    hdu = pyfits.open(images[0])[0]
    hdu.data = stack
    hdu.writeto('%s/%s' % (templates, name))
    if zips == 1:
        for image in images:
            os.system('rm %s' % image)
            os.system('rm %s' % (image.split('.fits')[0] + '_rm.fits'))
        recursive_del(input)
    if zips == 0:
        for image in images:
            os.system('rm %s' % (image.split('.fits')[0] + '_rm.fits'))

if __name__ == '__main__':
    maketemplate('template.fits')