# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:30:26 2019

@author: PAT
"""

# Import libraries
from pydub import AudioSegment
import librosa
import numpy as np
import matplotlib.pyplot as plt
from pydub.utils import get_array_type
import array
from scipy.io.wavfile import read
import soundfile as sf
import pyloudnorm as pyln
from crosscorrelation import pearson_def
from boxcounting4 import boxcounting
from bandpass2 import third_octave
import csv
import os

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

def segment(left_channel, right_channel):
    left_channel = np.array(left_channel.get_array_of_samples())
    right_channel = np.array(right_channel.get_array_of_samples())
    
    seg_length = 4096
#    ignore = len(left_channel)%range_index
#    endlength = len(left_channel) - ignore
#    print(len(left_channel))
#    print(number_index)
#    print(ignore)
#    print(endlength)
    
    start = 0

    vuL = []
    vuR = []
    drL = []
    drR = []
    peak_dbL = []
    peak_dbR = []
    rmsL = []
    rmsR = []
    pan = []
    xcor = []
    box = []
    rms_filterL = []
    rms_filterR = []
    pan_filter = []
    xcorr_filter = []
    box_filter = []
    i = 0
    while (1):
        end = start + seg_length
        segmentedL = left_channel[start:end] #ms
        segmentedR = right_channel[start:end] #ms
        scale = 20
#        print('length',len(left_channel[start:end]))
        if(len(left_channel[start:end]) < seg_length):
            print('length of last array (offset)',len(left_channel[start:end]))
#            print(i)
#            print('s',start)
#            print(end)
            break
#        print('s',start)
#        print('e',end)
#        print(len(left_channel[start:end]))
#        print(left_channel[start:end])
            
        print(i)
        
        vuL.append(vu_meter(segmentedL))
        vuR.append(vu_meter(segmentedL))
        drL.append(dynamicRange(segmentedR))
        drR.append(dynamicRange(segmentedR))
        peak_dbL.append(PPM(segmentedL))
        peak_dbR.append(PPM(segmentedL))
        rmsL.append(rms(segmentedL))
        rmsR.append(rms(segmentedR))
        pan.append(panning(segmentedL, segmentedR))
        xcor.append(pearson_def(segmentedL, segmentedR))
        box.append(boxcounting(segmentedL, segmentedR, scale))
        
        filteredSpeechL = third_octave(segmentedL)
        filteredSpeechR = third_octave(segmentedR)
        rms_filterL.append(rms(filteredSpeechL))
        rms_filterR.append(rms(filteredSpeechR))
        pan_filter.append(panning(filteredSpeechL, filteredSpeechR))
        box_filter.append(boxcounting(filteredSpeechL, filteredSpeechR, scale))
        xcorr_filter.append(pearson_def(filteredSpeechL, filteredSpeechR))
        
        start = end
        i+=1
        
#    seg_length = 4096
#    print([left_channel[x:x+seg_length] for x in range(0,len(left_channel),seg_length)][0])
    return zip(peak_dbL, peak_dbR, drL, drR, vuL, vuR, rmsL, rmsR, pan, xcor, box, rms_filterL, rms_filterR, pan_filter, box_filter, xcorr_filter)

def main():
# =============================================================================
# run by music
# =============================================================================
#    files_path = 'D:/Pat/Germany Intern/Training/4. Armin van Buuren/3minNorm/UMF Miami (2017)/'
#    file_name = 'This Is What Vendetta Feels Like'
#    file_type = '.mp3'
#    fullfilename = files_path + file_name + file_type
#    set_mu_path = os.path.basename(os.path.split(os.path.dirname(files_path))[-1])
#    norm_folder = os.path.split(os.path.dirname(files_path))[-2]
#    dj_name = os.path.basename(os.path.split(os.path.dirname(norm_folder))[-1])
#    print(set_mu_path)
#    print(dj_name)
#    print(file_name)
#    sound = AudioSegment.from_file(fullfilename)
#    if sound.channels == 2:
#        # stereo signal to two mono signal for left and right channel
#        split_sound = sound.split_to_mono()
#        left_channel = split_sound[0]
#        right_channel = split_sound[1]
#               
#        print('Extracting')
#        fea_name = ['peak_dbL', 'peak_dbR', 'drL', 'drR', 'vuL', 'vuR', 'rmsL', 'rmsR', 'pan', 'xcor', 'box', 'rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
#        zipped = segment(left_channel, right_channel) # by array
#        unzipped = list(zip(*zipped))
#        
#        dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_mu_path + '/' + file_name + '/'
#        os.makedirs(dirname, exist_ok = True)
#        for i in range(len(unzipped)):
#            with open(dirname + file_name + ' ' + str(fea_name[i]) + '.csv', 'w', newline = '') as fp:
#                a = csv.writer(fp, delimiter = ',')
#                a.writerows(map(lambda x: [x], unzipped[i]))
    
# =============================================================================
# run by set music
# =============================================================================
    
    set_music_path = 'D:/Pat/Germany Intern/Training/4. Armin van Buuren/3minNorm/UMF Miami (2019)'
    dj_name = os.path.basename(os.path.split(os.path.dirname(set_music_path))[-2])
    set_music_name = os.path.basename(set_music_path)
    print('set_music_name =', set_music_name)
    set_music = os.listdir(set_music_path)
#    print(set_music)
#    for music_path in set_music:
    i = 0
    while i < len(set_music):
#        print(set_music[i])
        full_mu_path = set_music_path + '/' + set_music[i]
        if ".mp3" in set_music[i]:
            music_name = set_music[i].replace('.mp3','')
        elif ".m4a" in set_music[i]:
            music_name = set_music[i].replace('.m4a','')
        if (".mp3" in set_music[i]) == True or (".m4a" in set_music[i]) == True:
            print(music_name)
            sound = AudioSegment.from_file(full_mu_path) #also read file
            if sound.channels == 1:
                continue
            # stereo signal to two mono signal for left and right channel
            split_sound = sound.split_to_mono()
            left_channel = split_sound[0]
            right_channel = split_sound[1]
            
            print('========== Extracting ===========')
            fea_name = ['peak_dbL', 'peak_dbR', 'drL', 'drR', 'vuL', 'vuR', 'rmsL', 'rmsR', 'pan', 'xcor', 'box', 'rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
            zipped = segment(left_channel, right_channel) 
            unzipped = list(zip(*zipped))
    
            dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_music_name + '/' + music_name + '/'
            os.makedirs(dirname, exist_ok = True)
            for j in range(len(fea_name)):
                with open(dirname + music_name + ' ' + str(fea_name[j]) + '.csv', 'w', newline = '') as fp:
                    a = csv.writer(fp, delimiter = ',')
                    a.writerows(map(lambda x: [x], unzipped[j]))
        i+=1
    
# =============================================================================
# run by dj
# =============================================================================
#    dj_name = '4. Armin van Buuren'
#    djpath = 'D:/Pat/Germany Intern/Training/'+ dj_name +'/3minNorm/'
#    set_music = os.listdir(djpath)
#    i = 1
#    while i < len(set_music):
#        setmusic = djpath + set_music[i]
#        if os.path.isdir(setmusic):
#            music_name_in_set = os.listdir(setmusic)
#            print(set_music[i])
##            print(music_name_in_set)
#            for music in music_name_in_set:
#                full_mu_path = setmusic + '/' + music
#                if (".mp3" in full_mu_path) == True or (".m4a" in full_mu_path) == True:
##                    print(full_mu_path)
#                    music_name_file = os.path.basename(full_mu_path)
#                    if ".mp3" in music_name_file:
#                        music_name = music_name_file.replace('.mp3','')
#                    elif ".m4a" in music_name_file:
#                        music_name = music_name_file.replace('.m4a','')
#                    
#                    sound = AudioSegment.from_file(setmusic + '/' + music_name_file)
#                    if sound.channels == 1:
#                        continue
#                    print(music_name)
#                    # stereo signal to two mono signal for left and right channel
#                    split_sound = sound.split_to_mono()
#                    left_channel = split_sound[0]
#                    right_channel = split_sound[1]
#                    
#                    # write to individual csv
#                            
#                    print('========== Extracting ===========')
#                    fea_name = ['peak_dbL', 'peak_dbR', 'drL', 'drR', 'vuL', 'vuR', 'rmsL', 'rmsR', 'pan', 'xcor', 'box', 'rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
#                    zipped = segment(left_channel, right_channel) # by array
#                    unzipped = list(zip(*zipped))
#
#                    dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_music[i] + '/' + music_name + '/'
#                    os.makedirs(dirname, exist_ok = True)
#                    for j in range(len(fea_name)):
#                        with open(dirname + music_name + ' ' + str(fea_name[j]) + '.csv', 'w', newline = '') as fp:
#                            a = csv.writer(fp, delimiter = ',')
#                            a.writerows(map(lambda x: [x], unzipped[j]))
#            i += 1
    
if __name__== "__main__":
    main()
