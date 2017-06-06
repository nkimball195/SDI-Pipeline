#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:46:49 2017

@author: noah
"""
from astropy.io import fits
import astroscrappy
import pyfits
hdulist = fits.open('/home/noah/image0.fits')
data = hdulist[0].data
mask = astroscrappy.detect_cosmics(data, sigclip=4.5, sigfrac=0.3, niter=1)
#astroscrappy.
print data
print mask
#print data[mask]
#hdu = pyfits.PrimaryHDU(image)
#hdu.writeto("new.fits")
clist=[]
for i in range(len(mask[0])):
    for j in range(len(mask[0][0])):
        if mask[0][i][j] == True:
            clist.append(i)
            print mask[1][i][j], data[i][j], 'i =', i, 'j =', j, '    DELTA =', data[i][j]-mask[1][i][j] 
astroscrappy.detect_cosmics()