import os

from .sound_wav import sound_wav_handle
from .wav_note import wav_note_handle
from .note_music import note_music_handle

class back_handle:
    '''
    The only class of back_handle
    '''
    def __init__(self,musicname='default'):
        self.Base_Dir=os.getcwd() #path
        self.music_name=musicname #name
        #class init
        self.recorder=sound_wav_handle.Recorder() 
        self.recorder.set_name(musicname)
        self.transcriber=wav_note_handle.Transcriber()
        self.composer= note_music_handle.Music()

    #recorder sound_wav function
    def start_record(self):
        self.recorder.start()
    def stop_record(self):
        self.recorder.stop()
        self.recorder.save(os.path.join(self.Base_Dir),'sound_wav/doc_wav',self.music_name+'.wav')
    

    #transcriber wav_note function
    def get_notes(self,file_name=None):
        if file_name==None:
            file_name=os.path.join(self.Base_Dir),'sound_wav/doc_wav',self.music_name+'.wav'
            self.transcriber.set_filename(file_name)
            notes,durations=self.transcriber.transcribe()
            durations=[i*2 for i in durations]
            return [tuple(i) for i in zip(notes,durations)]

    #composer note_music function
    def choose_program(self,program=0):
        '''
        设置乐器
        '''
        self.composer.set_program(program)

    def wav_sound(self):
        if os.path.exists(os.path.join(self.composer.save_path,self.composer.name+'.mid')):
            self.composer.play_midi()
    def mid_wav(self):
        if os.path.exists(os.path.join(self.composer.save_path,self.composer.name+'.mid')):
            self.composer.transfer_wav()


if __name__=="__main__":

    name=input("1.init: input music name. Needn't .wav or .mid.")
    Back_Handle=back_handle(name)
    print("init success")

    input('2.recorder in record_wav: Enter to start record, enter again to stop record')
    Back_Handle.start_record()
    print("start")
    input()
    Back_Handle.stop_record()
    print("stop")
    
    print("3.transcriber in wav_note")
    Note=Back_Handle.get_notes()
    print("got notes")

    print("4.composer in wav_sound")
    Back_Handle.choose_program(0)
    Back_Handle.wav_sound()
    print("5.composer in wav_sound")
    Back_Handle.mid_wav()