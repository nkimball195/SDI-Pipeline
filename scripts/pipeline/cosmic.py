#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:46:49 2017

@author: noah
"""
from astropy.io import fits
import astroscrappy
import pyfits
hdulist = pyfits.open('/home/noah/Desktop/pipeline/input/crr.fits')
data = hdulist[0].data
image = astroscrappy.detect_cosmics(data)
print image
#hdu = pyfits.PrimaryHDU(image)
#hdu.writeto("new.fits")