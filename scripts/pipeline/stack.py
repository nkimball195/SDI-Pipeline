#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 11:16:21 2017

@author: noah
"""
import pyfits
import numpy as np
import os
from pipeline import *

stack_name = 'template.fits'
input_path = input
output_path = templates

images = []
for root, dirs, files in os.walk(input_path):
    for file in files:
        if file.endswith('.fits'):
            file = os.path.join(root, file)
            images.append(file)

stack = []
for image in range(len(images)):

   stack.append(pyfits.open(images[image])[0].data.copy())

stack = np.median(np.array(stack),0)

print stack


hdu = pyfits.open(images[0])[0]

hdu.data = stack

hdu.writeto('%s/%s' % (output_path, stack_name))
