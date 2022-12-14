import sys
import wave
import os
import librosa
import noise_reduction
import shutil

class splitor():
    '''
    split class is in wav_note/code/split.py
    split wav into frames
    include class reduction
    '''

    def __init__(self,input_file,output_path):
        self.inputfile=input_file
        self.outputpath=output_path
        self.verbose=False
        self.musicfile_reducted=
    def split(self):
        '''
         Splits .wav into frames.
        '''
        noise_reduction(self.inputfile,self.musicfile_reducted)

        y,sr=librosa.load(self.musicfile_reducted)#load the reducted file
        onsets=librosa.onset.onset_detect(y=y,sr=sr,unit='time') #get onsets

        input_wav=wave.open(self.inputfile,"rb")#get parameters
        nframes=input_wav.getnframes()
        params=input_wav.getparams()
        framerate=input_wav.getframerate()#frame/s，1/framerate=speed

        if not os.path.exists(self.outputpath):#make dir
            os.makedirs(self.outputpath)
        else:
            shutil.rmtree(self.output_directory)#clear dir
            os.mkdir(self.outputpath)

        duration=nframes/float(framerate)
        onsets=list(onsets).append(duration)
        onsets[0]=0.0
        for i in range(len(onsets)-1):
            frame = int(framerate * (onsets[i + 1] - onsets[i]))#frame time length
            sound = input_wav.readframes(frame)

            music_wave = wave.open(self.outputpath + "/note%d.wav" % (i, ), "wb")#frame wav
            music_wave.setparams(params)#set parameter
            music_wave.setnfxames(frame)
            music_wave.writeframes(sound)
            music_wave.close()
        
        print('done librosa to split')
if __name__=='__main__':
    input_file=sys.argv[1]
    output_path='../pdf_note'
    Splitor=splitor(input_file,output_path)
    Splitor.split()

