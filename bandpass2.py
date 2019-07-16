# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:09:14 2019

@author: PAT
"""

from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

def third_octave(speech):
    ## Filtering of the time series
    sampleRate = 44100.0
    nyquistRate = sampleRate/2.0 # 0.5 times the sampling frequency
        
    centerFrequency_Hz = np.array([39, 50, 63, 79, 99, 125, 157, 198, 250, 315, 397, 500, 630, 794, 1000, 1260, 1588, 2000, 2520, 3176, 4000, 5040, 6352, 8000, 10080, 12704, 16000])
    G = 2 #base-2 rules
    factor = np.power(G, 1.0/6.0)
    lowerCutoffFrequency_Hz=centerFrequency_Hz/factor
    upperCutoffFrequency_Hz=centerFrequency_Hz*factor
    all_filter = []

#    ##fig=plt.figure()
#    ##plt.title('Speech Signal')
#    ##plt.plot(speech)
#    ##plt.show()
#    plt.figure()
#    plt.ylabel('Magnitude [dB]')
#    plt.xlabel('Frequency [rad/sample]')
#    plt.title('Digital filter frequency response')
#    plt.grid()
#    plt.axis([-0.2, 3.2, -80, 20])
    
    for lower,upper in zip(lowerCutoffFrequency_Hz, upperCutoffFrequency_Hz):
        
        # Design filter
        sos = signal.butter( N=4, Wn=np.array([lower, upper])/nyquistRate, btype='bandpass', analog=False, output='sos');
    
#        # Compute frequency response of the filter.
        w, h = signal.sosfreqz(sos)
#        
##        for i in range(len(h)):
##            if h[i] == 0j:
##                h[i] = min(j for j in h if j > 0)
##                    
#        plt.plot(w, 20 * np.log10(abs(h)/max(h)), 'b')
    
        # Filter signal
        filteredSpeech = signal.sosfiltfilt(sos, speech)
        
        for i in filteredSpeech:
            all_filter.append(i)
#    plt.plot(all_filter)   
#    plt.figure()
#    plt.title('Third Octave-band Filtered Speech')
#    plt.plot(filteredSpeech)
    
#    new = np.round(all_filter).astype('int16')
#    new_sound = sound._spawn(new) 
#    new_sound.export("music/clicks.mp3", format="mp3")
#    print(all_filter)
    return all_filter

#files_path = 'D:/Pat/Germany Intern/music/'
#file_name = 'filters'
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
#soundd= np.array(sound.get_array_of_samples())
#print(soundd)
#filteredSpeechL = third_octave(left_channel)
#filteredSpeechR = third_octave(right_channel)


#print('RMS for left channel', rms(filteredSpeechL))
#print('RMS for right channel', rms(filteredSpeechR))
#print('panning' , panning(filteredSpeechL, filteredSpeechR))
##boxcounting(filteredSpeechL, filteredSpeechR)
#print(pearson_def(filteredSpeechL, filteredSpeechR))

###########################################
#samples  = np.zeros(4096)
#samples[2048] = 1
#new_sound = sound._spawn(samples)
#new_sound.export("music/zero.mp3", format="mp3")
#filteredSpeechL = third_octave(np.array(sound.get_array_of_samples()), 'L')
#filteredSpeechL = np.round(filteredSpeechL).astype('int16')
#new_sound = sound._spawn(filteredSpeechL)
#
#new_sound.export("music/zerofilter2.mp3", format="mp3")

#count = 0
#for i in range(len(np.array(sound.get_array_of_samples()))):
#    if np.array(sound.get_array_of_samples())[i] == 1:
#        print(np.array(sound.get_array_of_samples())[i])
#        count += 1
#print(count)
