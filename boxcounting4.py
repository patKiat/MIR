# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 16:00:28 2019

@author: PAT
"""

import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from collections import OrderedDict

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

#files_path = 'D:/Pat/Germany Intern/Training/4. Armin van Buuren/norm/Armin-Tom-2013-norm/'
#file_name = 'Armin van Buuren presents Gaia – Humming The Lights_78089661 - Armin van Buuren'
#file_type = '.mp3'
#fullfilename = files_path + file_name + file_type
#sound = AudioSegment.from_file(fullfilename) #also read file
##sound = np.round(sound*20)
## stereo signal to two mono signal for left and right channel
#split_sound = sound.split_to_mono()
#left_channel = np.array(split_sound[0].get_array_of_samples())
#right_channel = np.array(split_sound[1].get_array_of_samples())
##norm and scale up
#scale = 20
##boxcounting(left_channel, right_channel, scale)
#
#    
#total_index = len(left_channel) #Length of audio in msec
#no_segment = 4096
#range_index = int(total_index/no_segment)
#start = 0
#count = 0
#box = []
#
#for i in range(no_segment):
#    end = start + range_index
#    segmentedL = left_channel[start:end] #ms
#    segmentedR = right_channel[start:end] #ms
#    
#    scale = 20
#    
##        print('count',count)
##        print(panning(segmentedL, segmentedR))
##        print(pearson_def(segmentedL, segmentedR))
#    print('segment no.' + str(i))
#    box.append(boxcounting(segmentedL, segmentedR, scale))
##    box_filter.append(boxcounting(filteredSpeechL, filteredSpeechR, scale))
#    
#    start = end
#    count += 1
#    
#print(box)
