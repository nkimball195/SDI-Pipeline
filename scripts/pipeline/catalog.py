#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 23:38:20 2017

@author: noah
"""

import os
from astropy.io import fits
from pipeline import *

def catalog():
    if os.path.exists('%s/run.log' % logs) == False or os.stat('%s/run.log' % logs).st_size == 0:
        newoutput()
    log = getlog()
    output = getoutput()
    #Creating list of templates
    template_list = []
    for root, dirs, files in os.walk(templates):
        for file in files:
            if file.endswith('.fits'):
                file=os.path.join(root, file)
                template_list.append(file)
    
    #Checking templates for duplicates
    error = []
    err = 0
    for temp in template_list:
            hdulist = fits.open(temp)
            tempfilter=hdulist[0].header['FILTER']
            tempRA=hdulist[0].header['CAT-RA']
            tempDEC=hdulist[0].header['CAT-DEC']
            hdulist.close()
            othertemps=[]
            for i in template_list:
                if template_list.index(i) > template_list.index(temp):
                    othertemps.append(i)
            for temp2 in othertemps:
                hdulist = fits.open(temp2)
                temp2filter=hdulist[0].header['FILTER']
                temp2RA=hdulist[0].header['CAT-RA']
                temp2DEC=hdulist[0].header['CAT-DEC']
                hdulist.close()
                if tempfilter==temp2filter and tempRA==temp2RA and tempDEC==temp2DEC and temp != temp2:
                    error.append("Error Duplicate Template: %s, %s" % (temp, temp2))
                    err = 1
    if err == 1:
        for i in range(len(error)):
            print error[i]
            with open(log, 'a') as file:
                file.write('\n%s\n' % error[i])
        print "Error: Check image catalog file"
        quit()
    
    #Making output path for image copies
    if os.path.exists('%s/0.original' % output) == False:
        os.mkdir('%s/0.original' % output)
    
    #Decompress files and images
    for root, dirs, files in os.walk(input):
        for file in files:
            if file.endswith('.zip'):
                zips=os.path.join(root, file)
                os.system('unzip %s -d %s' % (zips, input))
    #            os.rename(zips, '%s/0.original/%s' % (output, file))
    for root, dirs, files in os.walk(input):
        for file in files:
            if file.endswith('.fz'):
                fz=os.path.join(root, file)
                os.system('funpack %s' % fz)
                os.system('rm %s' % fz)
    
    #Importing input images and creating list
    images=[]
    for root, dirs, files in os.walk(input):
        for file in files:
            if file.endswith('.fits'):
                image=os.path.join(root, file)
                os.rename(image, '%s/0.original/%s' % (output, file))
                image='%s/0.original/%s' % (output, file)
                images.append(image)
    images.sort()
    #Removing empty folders from input folder
    def recursive_del(folder):
        loop=[]
        for root, dirs, files in os.walk(folder):
            for dir in dirs:
                dir=os.path.join(root, dir)
                loop.append(len(os.listdir(dir)))
        if 0 in loop:
            delete_empty(folder)
            recursive_del(folder)
        else:
            print ""
    def delete_empty(folder):
        for root, dirs, files in os.walk(folder):
            for dir in dirs:
                dir=os.path.join(root, dir)
                if len(os.listdir(dir)) == 0:
                    os.rmdir(dir)
    recursive_del(input)
    
    #Writing header values
    for image in images:
        hdulist = fits.open(image)
        imagehdu=hdulist[0]
        imagefilter=hdulist[0].header['FILTER']
        imageRA=hdulist[0].header['CAT-RA']
        imageDEC=hdulist[0].header['CAT-DEC']
        imagehdu.header['SDI_NAME'] = '%s' % image.split('/')[-1]
        imagehdu.header['SDI_TEMP'] = 'NA'
        hdulist.writeto('%s' % image, clobber=True)
        hdulist.close()
        for temp in template_list:
            hdulist = fits.open(temp)
            tempfilter=hdulist[0].header['FILTER']
            tempRA=hdulist[0].header['CAT-RA']
            tempDEC=hdulist[0].header['CAT-DEC']
            hdulist.close()
            if tempRA==imageRA and tempDEC==imageDEC and tempfilter==imagefilter:
                hdulist = fits.open(image)
                hdu=hdulist[0]
                hdu.header['SDI_TEMP'] = '%s' % temp.split('/')[-1]
                hdulist.writeto('%s' % image, clobber=True)
                hdulist.close()          
            else:
                print "Couldn't find template for '%s'" % (image)
    updatelog()
    
if __name__ == "__main__":
    catalog()
