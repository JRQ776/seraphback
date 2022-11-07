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

    def split(self):
        '''
         Splits .wav into frames.
        '''
        print('In split function to start')

        #noise reduction
        print('start to noise reduction')
        noise_reduction(self.inputfile,self.outputpath)
        print('done for noise reducton')

        print('librosa to split')

        print('done librosa to split')
if __name__=='__main__':
    input_file=sys.argv[1]
    output_path='../pdf_note'
    Splitor=splitor(input_file,output_path)
    Splitor.split()

