
# coding: utf-8

# In[13]:


import os

# =============================================================================
# run by set music
# =============================================================================
 
#    set_music_path = 'D:/Pat/Germany Intern/Training/4. Armin van Buuren/3minNorm/UMF Miami (2019)'
#    dj_name = os.path.basename(os.path.split(os.path.dirname(set_music_path))[-2])
#    set_music_name = os.path.basename(set_music_path)
#    print('set_music_name =', set_music_name)
#    set_music = os.listdir(set_music_path)
#    print(set_music)
#    i = 0
#    while i < len(set_music):
# #        print(set_music[i])
#        full_mu_path = set_music_path + '/' + set_music[i]
#        if ".mp3" in set_music[i]:
#            music_name = set_music[i].replace('.mp3','')
#        elif ".m4a" in set_music[i]:
#            music_name = set_music[i].replace('.m4a','')

#             dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_music[i] + '/' + music_name + '/'
           
#             fea_name_filter = ['rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
#             for y in range(len(fea_name_filter)):
#                 filename = dirname + music_name + ' ' + str(fea_name_filter[y]) + '.csv'
#                 print(filename)
#                 if os.path.exists(filename):
#                     os.remove(filename)
#                     print('delete')
#                 else:
#                     print('Does not exist before')
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

                dirname = 'D:/Pat/Germany Intern/dataset/' + dj_name + '/' + set_music[i] + '/' + music_name + '/'
#            
                fea_name_filter = ['rms_filter L', 'rms_filter R', 'pan_filter', 'box_filter', 'xcorr_filter']
                for y in range(len(fea_name_filter)):
                    filename = dirname + music_name + ' ' + str(fea_name_filter[y]) + '.csv'
                    print(filename)
                    if os.path.exists(filename):
                        os.remove(filename)
                        print('delete')
                    else:
                        print('Does not exist before')

        i += 1

