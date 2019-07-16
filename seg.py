# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:07:51 2019

@author: PAT
"""
import os
from pydub import AudioSegment
import numpy as np

dj_name = '4. Armin van Buuren'
djpath = 'D:/Pat/Germany Intern/Training/'+ dj_name +'/!Normalized/'
#djpath = 'E:/Training/'+ dj_name +'/!Normalized/'
set_music = os.listdir(djpath)
i = 0
while i < len(set_music):
    setmusic = djpath + set_music[i]
    if os.path.isdir(setmusic):
        music_name_in_set = os.listdir(setmusic)
#            print(set_music[i])
#            print(music_name_in_set)
        for music in music_name_in_set:
            full_mu_path = setmusic + '/' + music
            set_mu_name = os.path.basename(setmusic)
            if (".mp3" in full_mu_path) == True or (".m4a" in full_mu_path) == True:
#                    print(full_mu_path)
                music_name_file = os.path.basename(full_mu_path)
                if ".mp3" in music_name_file:
                    music_name = music_name_file.replace('.mp3','')
                elif ".m4a" in music_name_file:
                    music_name = music_name_file.replace('.m4a','')
                
                
                song = AudioSegment.from_file(full_mu_path)
                if len(song) >= 180000: # 1 min = 60000 msec
                    print(music_name)
                    halfway_point = len(song)/2
                    
    #                startms = halfway_point-90000 # msec
    #                endms = halfway_point+90000 # msec
    #                
    #                startMin = (int)(startms/60000)
    #                startSec = (int)((startms / 1000) % 60)
    #                print(startMin)
    #                print(startSec)
    #                
    #                endMin = (int)(endms/60000)
    #                endSec = (int)((endms / 1000) % 60)
    #                print(endMin)
    #                print(endSec)
    #                
    #                # Time to miliseconds
    #                startTime = startMin*60*1000+startSec*1000
    #                endTime = endMin*60*1000+endSec*1000
                    
                    startTime = halfway_point-90000-1 # msec
                    endTime = halfway_point+90000+1 # msec
                    
#                    # extracting segment
                    extract = song[startTime:endTime]
                    split_sound = extract.split_to_mono()
                    left_channel = split_sound[0]
                    right_channel = split_sound[1]
#                    print(len(np.array(left_channel.get_array_of_samples()))/4096)
#                    print(startTime)
#                    print(endTime)
                
                    dirname = 'D:/Pat/Germany Intern/Training/' + dj_name + '/3minNorm/' + set_mu_name
                    os.makedirs(dirname, exist_ok = True)
                    # Saving
                    extract.export( 'D:/Pat/Germany Intern/Training/' + dj_name + '/3minNorm/' + set_mu_name + '/' + music_name + '.mp3', format="mp3")
#                    songs = AudioSegment.from_file('D:/Pat/Germany Intern/Training/' + dj_name + '/3minNorm/' + set_mu_name + '/' + music_name + '.mp3')
#                    split_sound = songs.split_to_mono()
#                    left_channel = split_sound[0]
#                    right_channel = split_sound[1]
#                    print(len(songs))
#                    print(len(np.array(left_channel.get_array_of_samples())))
#
#                    
#            break
#        break
        i += 1
