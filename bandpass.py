# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:06:34 2019

@author: PAT
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:09:14 2019

@author: PAT
"""

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
#from features import *
import csv
import os

def third_octave(speech):
    ## Filtering of the time series
    sampleRate = 44100.0
    nyquistRate = sampleRate/2.0 # 0.5 times the sampling frequency
        
    centerFrequency_Hz = np.array([39, 50, 63, 79, 99, 125, 157, 198, 250, 315, 397, 500, 630, 794, 1000, 1260, 1588, 2000, 2520, 3176, 4000, 5040, 6352, 8000, 10080, 12704, 16000])
    G = 2 #base-2 rules
    factor = np.power(G, 1.0/6.0)
    lowerCutoffFrequency_Hz=centerFrequency_Hz/factor
    upperCutoffFrequency_Hz=centerFrequency_Hz*factor
    all_bandpass = []
    
    for lower,upper in zip(lowerCutoffFrequency_Hz, upperCutoffFrequency_Hz):
        
        # Design filter
        sos = signal.butter( N=4, Wn=np.array([lower, upper])/nyquistRate, btype='bandpass', analog=False, output='sos');
    
        # Compute frequency response of the filter.
        w, h = signal.sosfreqz(sos)
    
        # Filter signal
        filteredSpeech = signal.sosfiltfilt(sos, speech)
        all_bandpass.append(filteredSpeech)

    return all_bandpass

#files_path = 'D:/Pat/Germany Intern/'
#file_name = 'Sander1'
#file_type = '.mp3'
#fullfilename = files_path + file_name + file_type
#sound = AudioSegment.from_file(fullfilename) #also read file
#
### stereo signal to two mono signal for left and right channel
#split_sound = sound.split_to_mono()
#left_channel = split_sound[0]
#right_channel = split_sound[1]
#left_channel = np.array(left_channel.get_array_of_samples())
#right_channel = np.array(right_channel.get_array_of_samples())
#filteredSpeechL = third_octave(left_channel)
#filteredSpeechR = third_octave(right_channel)
##print(len(filteredSpeechL))
#
#scale = 20
#rms_filterL = []
#rms_filterR = []
#pan_filter = []
#xcorr_filter = []
#box_filter = []
#third_octave_filter = []
#for i in range(27):
#    rms_filterL.append(rms(filteredSpeechL[i]))
#    rms_filterR.append(rms(filteredSpeechR[i]))
#    pan_filter.append(panning(filteredSpeechL[i], filteredSpeechR[i]))
#    box_filter.append(boxcounting(filteredSpeechL[i], filteredSpeechR[i], scale))
#    xcorr_filter.append(pearson_def(filteredSpeechL[i], filteredSpeechR[i]))

#third_octave_filter.append(rms_filterL)
#third_octave_filter.append(rms_filterR)
#third_octave_filter.append(pan_filter)
#third_octave_filter.append(box_filter)
#third_octave_filter.append(xcorr_filter)
##print(rms_filterL)
#
#fea_name = ['rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
#header = []
#for i in range(27):
#    header.append('band ' + str(i+1))
#    
#for i in range(len(third_octave_filter)):
#    print(third_octave_filter[i])
#    
#    with open('testcsv/'+fea_name[i] + '.csv', 'a', newline='') as csvFile:
#        file_is_empty = os.stat('testcsv/'+fea_name[i] + '.csv').st_size == 0
#        writer = csv.writer(csvFile, delimiter=',')
#        if file_is_empty:
#            writer.writerow(i for i in header)
#        writer.writerow(third_octave_filter[i])
#    csvFile.close()