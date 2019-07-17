# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:47:03 2019

@author: PAT
"""

# Import libraries
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt
from pydub.utils import get_array_type
import array
from scipy.io.wavfile import read
import soundfile as sf
import pyloudnorm as pyln
from bandpass import third_octave
from features import *
import csv
import os

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

    rms_filterL = []
    rms_filterR = []
    pan_filter = []
    xcorr_filter = []
    box_filter = []
    all_filter = []
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
        
        filteredSpeechL = third_octave(segmentedL)
        filteredSpeechR = third_octave(segmentedR)
        rms_filterL = []
        rms_filterR = []
        pan_filter = []
        xcorr_filter = []
        box_filter = []
        third_octave_filter = []
        for band in range(27):
            rms_filterL.append(rms(filteredSpeechL[band]))
            rms_filterR.append(rms(filteredSpeechR[band]))
            pan_filter.append(panning(filteredSpeechL[band], filteredSpeechR[band]))
            box_filter.append(boxcounting(filteredSpeechL[band], filteredSpeechR[band], scale))
            xcorr_filter.append(pearson_def(filteredSpeechL[band], filteredSpeechR[band]))
            
        third_octave_filter.append(rms_filterL)
        third_octave_filter.append(rms_filterR)
        third_octave_filter.append(pan_filter)
        third_octave_filter.append(box_filter)
        third_octave_filter.append(xcorr_filter)
        all_filter.append(third_octave_filter)
        start = end
        i+=1
    
#    seg_length = 4096
#    print([left_channel[x:x+seg_length] for x in range(0,len(left_channel),seg_length)][0])
#    return zip(peak_dbL, peak_dbR, drL, drR, vuL, vuR, rmsL, rmsR, pan, xcor, box, rms_filterL, rms_filterR, pan_filter, box_filter, xcorr_filter)
    return all_filter

def main():
# =============================================================================
# run by music
# =============================================================================
#    files_path = 'D:/Pat/Germany Intern/Training/4. Armin van Buuren/3minNorm/Tomorrowland (2013)/'
#    file_name = 'Apache'
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
##        fea_name = ['peak_dbL', 'peak_dbR', 'drL', 'drR', 'vuL', 'vuR', 'rmsL', 'rmsR', 'pan', 'xcor', 'box', 'rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
#        fea_name = ['peak_dbL', 'peak_dbR', 'drL', 'drR', 'vuL', 'vuR', 'rmsL', 'rmsR', 'pan', 'xcor', 'box']
#        zipped = segment(left_channel, right_channel) # by array
#        unzipped = list(zip(*zipped))
#        
#        dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_mu_path + '/' + file_name + '/'
#        os.makedirs(dirname, exist_ok = True)
#        for i in range(11):
#            with open(dirname + file_name + ' ' + str(fea_name[i]) + '.csv', 'w', newline = '') as fp:
#                a = csv.writer(fp, delimiter = ',')
#                a.writerows(map(lambda x: [x], unzipped[i]))
#        
#        all_filter = unzipped[11]
#        fea_name_filter = ['rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
#        header = []
#        for i in range(27):
#            header.append('band ' + str(i+1))
#        
#        for i in range(len(all_filter)):
##            print(all_filter[i])
#            for j in range(len(all_filter[i])):  # 5 features
#                #print(fea_name_filter[j])
#                #print(all_filter[i][j])
##                for k in range(len(all_filter[i][j])): # 27 values
##                    print(all_filter[i][j][k])
#                with open(dirname + file_name + ' ' + str(fea_name_filter[j]) + '.csv', 'a', newline='') as csvFile:
##                    file_is_empty = os.stat(dirname + file_name + ' ' + str(fea_name_filter[j]) + '.csv').st_size == 0
#                    writer = csv.writer(csvFile, delimiter=',')
##                    if file_is_empty:
##                        writer.writerow(l for l in header)
#                    writer.writerow(all_filter[i][j])
#                csvFile.close()
    
# =============================================================================
# run by set music
# =============================================================================
    
#    set_music_path = 'D:/Pat/Germany Intern/Training/4. Armin van Buuren/3minNorm/UMF Miami (2019)'
#    dj_name = os.path.basename(os.path.split(os.path.dirname(set_music_path))[-2])
#    set_music_name = os.path.basename(set_music_path)
#    print('set_music_name =', set_music_name)
#    set_music = os.listdir(set_music_path)
##    print(set_music)
##    for music_path in set_music:
#    i = 0
#    while i < len(set_music):
##        print(set_music[i])
#        full_mu_path = set_music_path + '/' + set_music[i]
#        if ".mp3" in set_music[i]:
#            music_name = set_music[i].replace('.mp3','')
#        elif ".m4a" in set_music[i]:
#            music_name = set_music[i].replace('.m4a','')
#        if (".mp3" in set_music[i]) == True or (".m4a" in set_music[i]) == True:
#            print(music_name)
#            sound = AudioSegment.from_file(full_mu_path) #also read file
#            if sound.channels == 1:
#                continue
#            # stereo signal to two mono signal for left and right channel
#            split_sound = sound.split_to_mono()
#            left_channel = split_sound[0]
#            right_channel = split_sound[1]
#            
#            print('========== Extracting ===========')
#            fea_name = ['peak_dbL', 'peak_dbR', 'drL', 'drR', 'vuL', 'vuR', 'rmsL', 'rmsR', 'pan', 'xcor', 'box']
#            zipped = segment(left_channel, right_channel) 
#            unzipped = list(zip(*zipped))
#    
#            dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_music_name + '/' + music_name + '/'
#            os.makedirs(dirname, exist_ok = True)
#            for j in range(11):
#                with open(dirname + music_name + ' ' + str(fea_name[j]) + '.csv', 'w', newline = '') as fp:
#                    a = csv.writer(fp, delimiter = ',')
#                    a.writerows(map(lambda x: [x], unzipped[j]))
#                    
#            all_filter = unzipped[11]
#            
#            fea_name_filter = ['rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
#            header = []
#            for x in range(27):
#                header.append('band ' + str(x+1))
#            
#            for x in range(len(all_filter)):
#    #            print(all_filter[x])
#                for y in range(len(all_filter[x])):  # 5 features
#                    #print(fea_name_filter[y])
#                    #print(all_filter[x][y])
#    #                for k in range(len(all_filter[i][j])): # 27 values
#    #                    print(all_filter[i][j][k])
#                    with open(dirname + music_name + ' ' + str(fea_name_filter[y]) + '.csv', 'a', newline='') as csvFile:
##                        file_is_empty = os.stat(dirname + music_name + ' ' + str(fea_name_filter[y]) + '.csv').st_size == 0
##                        if file_is_empty:
##                            writer.writerow(l for l in header)
#                        writer = csv.writer(csvFile, delimiter=',')
#                        writer.writerow(all_filter[x][y])
#                    csvFile.close()
#        i+=1
    
# =============================================================================
# run by dj
# =============================================================================
    dj_name = '6. Tiesto'
    djpath = 'D:/Pat/Germany Intern/Training/'+ dj_name +'/3minNorm/'
    set_music = os.listdir(djpath)
    i = 0
    while i < len(set_music):
        setmusic = djpath + set_music[i]
        if os.path.isdir(setmusic):
            music_name_in_set = os.listdir(setmusic)
            print(set_music[i])
#            print(music_name_in_set)
            for music in music_name_in_set:
                full_mu_path = setmusic + '/' + music
                if (".mp3" in full_mu_path) == True or (".m4a" in full_mu_path) == True:
#                    print(full_mu_path)
                    music_name_file = os.path.basename(full_mu_path)
                    if ".mp3" in music_name_file:
                        music_name = music_name_file.replace('.mp3','')
                    elif ".m4a" in music_name_file:
                        music_name = music_name_file.replace('.m4a','')
                    
                    sound = AudioSegment.from_file(setmusic + '/' + music_name_file)
                    if sound.channels == 1:
                        continue
                    print(music_name)
                    # stereo signal to two mono signal for left and right channel
                    split_sound = sound.split_to_mono()
                    left_channel = split_sound[0]
                    right_channel = split_sound[1]
                    
                    # write to individual csv
                            
                    print('========== Extracting ===========')
                            
                    all_filter = segment(left_channel, right_channel)
                    dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_music[i] + '/' + music_name + '/'
                    os.makedirs(dirname, exist_ok = True)
                    fea_name_filter = ['rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
                    
                    for x in range(len(all_filter)):
            #            print(all_filter[x])
                        for y in range(len(all_filter[x])):  # 5 features
#                            print(fea_name_filter[y])
#                            print(all_filter[x][y])
                            with open(dirname + music_name + ' ' + str(fea_name_filter[y]) + '.csv', 'a', newline='') as csvFile:
                                writer = csv.writer(csvFile, delimiter=',')
                                writer.writerow(all_filter[x][y])
                            csvFile.close()
                    
            i += 1
    
if __name__== "__main__":
    main()
