from os import path
import numpy as np
from pydub import AudioSegment
import wave
from scipy.io import wavfile


files_path = ''
file_name = 'Friendzone1'
file_type = '.mp3'
fullfilename = files_path + file_name + file_type
#fullfilename = "Friendzone.mp3"
#sound = AudioSegment.from_file(fullfilename) #also read file
# stereo signal to two mono signal for left and right channel
#split_sound = sound.split_to_mono()
#left_channel = np.array(split_sound[0].get_array_of_samples())
#right_channel = np.array(split_sound[1].get_array_of_samples())

#for i in left_channel:
#    print(i)

#print("Old info of segment")
#print(left_channel)
#print(right_channel)

#newfilename = "normalizedfull.mp3"

#def match_target_amplitude(sound, target_dBFS):
#    change_in_dBFS = target_dBFS - sound.dBFS
#    return sound.apply_gain(change_in_dBFS)
#
#sound = AudioSegment.from_file(fullfilename, "mp3")
#normalized_sound = match_target_amplitude(sound, 0.0)
#normalized_sound.export(newfilename, format="mp3")

#sound = AudioSegment.from_file(newfilename, "mp3") #also read file
## stereo signal to two mono signal for left and right channel
#split_sound = sound.split_to_mono()
#left_channel = np.array(split_sound[0].get_array_of_samples())
#right_channel = np.array(split_sound[1].get_array_of_samples())
#
#print("New info of segment")
#print(left_channel)
#print(right_channel)

##formula normalization
#newmin = -1
#newmax = 1
#leftmin = left_channel - min(left_channel)
#maxmin = max(left_channel) - min(left_channel)
#print(leftmin)
#print(maxmin)
#val = (leftmin/maxmin)*(newmax-newmin)+newmin
#for x in val:
#    print(x)

##decimal normalization
#j = 5
#val = []
#print(left_channel)
#print(max(left_channel))
#for l in left_channel:
#    v = float(l)/pow(10,j)
#    print(v)
#    val.append(v)
#print(val[-2])

newfilename = "music/normwav.mp3"
dst = "music/test.wav"
output = "music/norm.wav"

#convert mp3 to wav
sound = AudioSegment.from_mp3(fullfilename)
sound.export(dst, format="wav")
sr,data=wavfile.read(dst)
#convert to normalized 32 bit floating point (.wav)
normalized_x = data/np.abs(data).max()
for n in normalized_x:
    print(n)
wavfile.write(output,sr,normalized_x.astype(np.float32))
#a, b = wavfile.read("norm.wav")
#print(b)
#export wav as mp3
AudioSegment.from_wav(output).export(newfilename, format="mp3")

#test mp3 import
sound = AudioSegment.from_file(newfilename)
#print(sound.get_array_of_samples())
#split_sound = sound.split_to_mono()
#left_channel = np.array(split_sound[0].get_array_of_samples())
#right_channel = np.array(split_sound[1].get_array_of_samples())
#
#print(left_channel)
#print(right_channel)