# -*- coding: utf-8 -*-
"""
Created on Fri May 26 12:37:02 2017

@author: Noah
"""


import os
import numpy as np
import datetime
from astropy.io import fits

project_name = 'SDI'
header_id = 'SDI'
directory_script_path = os.path.realpath(__file__).replace('\\', '/')
directory = "scripts".join(directory_script_path.split("scripts")[:-1])
input = directory + 'input'
outputs = directory + 'output'
templates = directory + 'templates'
logs = directory + 'logs'

def gettime():
    return datetime.datetime.now().strftime("%Y-%m-%dT%Hh%Mm%Ss")

def createname(name):
    pipeline_name = name + '_' + gettime()
    return pipeline_name

def getlog():
    run_log = np.genfromtxt('%s/run.log' % logs, dtype=None)
    try:
        log = run_log[-1]
    except IndexError:
        with open('%s/run.log' % logs) as file:
            log = file.readline()
            log = log.rstrip('\n')
    log = '%s/%s' % (logs, log)
    return log  

def getoutput():
    log = getlog()
    with open('%s' % log) as file:
        line = file.readline()
        line = line.rstrip('\n')
        output = line.split(": ")[1]  
    return output

def getrecent():
    output = getoutput()
    output_folders = []
    for dir in os.listdir(output):
        dir = output + '/' + dir
        if os.path.isdir(dir) == True:
            output_folders.append(dir)
    output_folders.sort()
    recent = output_folders[-1]
    return recent

def newfolder(folder):
    output = getoutput()
    try:
        recent = getrecent()
        new = recent.split('/')[-1] 
        new =  "%s" % str(int(new[0:new.index('.')]) + 1)
    except IndexError:
        new = "0"
    new = '%s/%s.%s' %(output, new, folder)
    os.mkdir(new)

def newoutput(NAME=''):
    if NAME == '':
        name = createname(project_name)
    else:
        name = NAME
    log = open("%s/%s.log" % (logs, name), 'w')
    log.write("# " + "Output".ljust(9) + ": " + "%s/%s\n"% (outputs, name))
    log.close()
    if os.path.exists('%s/run.log' % logs) == False:
        with open('%s/run.log' % logs, 'w') as file:
            file.write('%s.log\n' % name)
    elif os.path.exists('%s/run.log' % logs) == True:
        with open('%s/run.log' % logs, 'a') as file:
            file.write('%s.log\n' % name)
    output = "%s/%s" % (outputs, name)
    os.mkdir(output)
        
def updatelog():
    log = getlog()
    output = getoutput()
    recent = getrecent()
    with open(log, 'w') as file:
        file.write("# " + "Output".ljust(9) + ": " + "%s\n"% output)
    keylist=[]
    for i in os.listdir(recent):
        i=os.path.join(recent, i)
        if i.endswith('.fits'):
            hdulist=fits.open(i)
            prihdr=hdulist[0].header
            for key in prihdr.keys():
                if key.startswith(header_id) and key not in keylist:
                    keylist.append(key)
                hdulist.close()
    for key in keylist:
        with open(log, 'a') as file:
            file.write('# ' + key.ljust(9) + ': ' + 'Column[%s]\n' % keylist.index(key))
    for i in sorted(os.listdir(recent)):
        i=os.path.join(recent, i)
        if i.endswith('.fits'):
            hdulist=fits.open(i)
            prihdr=hdulist[0].header
            logline=''
            for key in keylist: 
                try: 
                    logline+=(prihdr[key] + '    ')
                except KeyError:
                    logline+=('NA    ')
            with open(log, 'a') as file:
                file.write('%s\n' % logline)
            hdulist.close()
            
def getfiles(path, ext='', pre='', join=True):
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext) and file.startswith(pre):
                if join == True:
                    filelist.append(os.path.join(root, file))
                elif join == False:
                    filelist.append(file)
    return filelist

def getimages(path):
    return getfiles(path, ext='fits')    

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

def clear(path, q=False):
    if q == False:
        check = raw_input('Delete ALL files and folders from %s? [y/n]\n>>>' % path)
        if check == 'y' or check == 'Y':
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file != 'README':
                        file = os.path.join(root, file)
                        os.system('rm %s' % file)
            recursive_del(path)
        else:
            quit()
    elif q == True:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file != 'README':
                    file = os.path.join(root, file)
                    os.system('rm %s' % file)
        recursive_del(path)

def clearall(t=False):
    check = raw_input('Delete ALL input, output, and log files?[y/n]\n>>>')
    if check == 'y' or check == 'Y':
        clear(input, q=True)
        clear(outputs, q=True)
        clear(logs, q=True)
        if t == True:
            clear(templates)
    else:
        quit()