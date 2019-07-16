# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 14:55:58 2019

@author: PAT
"""
'''
"Crosscorrelation" is correlation between two series of the same length, with or without lags. "Correlation coefficient" is a normalized correlation. 
'''
# https://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
import numpy as np
from pydub import AudioSegment
import math
import pandas as pd
import pycorrelate as pyc

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

    return diffprod / math.sqrt(xdiff2 * ydiff2) #Sum[(x - avg_x) * (y - avg_y)] / sqrt((x - avg_x)^2 * (y - avg_y)^2)

#def corr(data1, data2):
#    "data1 & data2 should be numpy arrays."
#    mean1 = data1.mean() 
#    mean2 = data2.mean()
#    std1 = data1.std()
#    std2 = data2.std()
#
##     corr = ((data1-mean1)*(data2-mean2)).mean()/(std1*std2)
#    corr = ((data1*data2).mean()-mean1*mean2)/(std1*std2)
#    return corr


#files_path = 'D:/Pat/Germany Intern/Training/4. Armin van Buuren/norm/Armin-Tom-2013-norm/'
#file_name = 'Armin van Buuren presents Gaia – Humming The Lights_78089661 - Armin van Buuren'
#file_type = '.mp3'
#fullfilename = files_path + file_name + file_type
#sound = AudioSegment.from_file(fullfilename) #also read file
## stereo signal to two mono signal for left and right channel
#split_sound = sound.split_to_mono()
#left_channel = np.array(split_sound[0].get_array_of_samples())
#right_channel = np.array(split_sound[1].get_array_of_samples())
#
#print(pearson_def(left_channel, right_channel))
#print(left_channel)
#print(right_channel)


