# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:02:00 2019

@author: PAT
"""
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from collections import OrderedDict
import math

def rms(segmentedAudio):
    rms = np.sqrt(np.mean(np.array(segmentedAudio, dtype='int64')**2))
    if rms == 0:
        rms_db = 20*np.log10(0.0001)
    else:
        rms_db = 20*np.log10(rms)
    return rms_db
    
def PPM(segmentedAudio):
    peak = max(abs(segmentedAudio))
    return peak

def dynamicRange(segmentedAudio):
    ratio = abs(max(np.array(segmentedAudio))/min(np.array(segmentedAudio)))
    if ratio == 0:
        ratio = 0.00001
    dr = abs(10 * np.log10(ratio))
    return dr

# https://stackoverflow.com/questions/35543986/python-get-audio-pan-l-r
def ampradio_to_angle(x):
    """ converts ratio of amplitude of left and right channel to degree in radians """
    if x == 1:
        return 0
    else:
        return 2 * np.arctan((-1 * np.sqrt(2) * np.sqrt(x*x + 1) + x + 1) / (x - 1))

def rad_to_unit(x):
    """ scales -45° to 45° in radiants between -1 and 1 """
    return np.degrees(x)/45

def panning(segmentedL, segmentedR):
    idx = segmentedR != 0
#    print(segmentedR[idx])
#    if len(segmentedR[idx]) == 0:
#        ratio = 1e9 # some big number
#    else:
#        ratio = np.average(segmentedL[idx] / segmentedR[idx])
    ratio = np.average(segmentedL[idx] / segmentedR[idx])
    return rad_to_unit(ampradio_to_angle(ratio))

def vu_meter(segment):
    return 20 * np.log10(np.mean(abs(segment)))

def norm(arr):
    return arr/np.abs(arr).max()

def boxcounting(segmentedL, segmentedR, scale):
    scaleupL = np.round(norm(segmentedL) * scale, 1)
    scaleupR = np.round(norm(segmentedR) * scale, 1)
    # remove duplicate coordinate pair
    pair = list(OrderedDict.fromkeys(list(zip(scaleupL, scaleupR))))
    
    L = list(zip(*pair))[0]
    R = list(zip(*pair))[1]
    
#    plt.hist2d(L, R, bins=scale, cmap='Blues')
#    cb = plt.colorbar()
#    cb.set_label('counts in bin')
    # https://jakevdp.github.io/PythonDataScienceHandbook/04.05-histograms-and-binnings.html
    counts, xedges, yedges = np.histogram2d(L, R, bins=scale)
#    print(counts)
    # count number of elements that is not equal to zero
    countbox = np.count_nonzero(counts)
#    print('No. of box that has value =', countbox)
    return countbox

def pearson_def(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = np.average(x)
    avg_y = np.average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff
    #Sum[(x - avg_x) * (y - avg_y)] / sqrt((x - avg_x)^2 * (y - avg_y)^2)
    return diffprod / math.sqrt(xdiff2 * ydiff2) 

