from mido import Message, MidiFile, MidiTrack
import pygame
import os
import subprocess
import shutil
import sys
import melody_note.work.wav_note.music_transcriber

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR,'wav_note'))

bpm = 75

class Music:
    """
    melody：[音阶（0~127,音高：C调do为基准60） ，长度（浮点数）]
    name：歌曲名
    program：乐器代号
    bpm：节拍数（Beat Per Minute）
    """
    def __init__(self,melody=None,name='default',program=0,bpm=75,save_path=os.path.join(BASE_DIR,'compose_mid')):
        self.melody = melody
        self.name = name
        self.program = program
        self.bpm = bpm
        self.save_path = save_path
        if melody != None:
            self.mid = MidiFile()  # 创建MidiFile对象
            self.track = MidiTrack()  # 创建音轨
            self.mid.tracks.append(self.track)  # 把音轨加到MidiFile对象中
            self.track.append(Message('program_change', program=program, time=0)) #设置音色
            self.track.append(Message('note_on', note=64, velocity=64, time=32))  #音符起
            self.track.append(Message('note_off', note=64, velocity=127, time=32))#音符止
            for m in melody:
                self.play_note(m[0],m[1])
            self.save_mid()
    
    # 设置音乐名
    def set_name(self, name='default'):
        self.name = name
    
    # 设置旋律，格式为：[(音符、时长)] 例如：[(60,1),(63,2),(66,0.5),...]
    def set_melody(self, melody):
        self.melody = melody
        self.mid = MidiFile()  # 创建MidiFile对象
        self.track = MidiTrack()  # 创建音轨
        self.mid.tracks.append(self.track)  # 把音轨加到MidiFile对象中
        self.track.append(Message('program_change', program=self.program, time=0))
        self.track.append(Message('note_on', note=64, velocity=64, time=32))
        self.track.append(Message('note_off', note=64, velocity=127, time=32))
        for m in melody:
            self.play_note(m[0],m[1])
        self.save_mid()
    
    # 设置乐器代号，对应关系见https://blog.csdn.net/ruyulin/article/details/84103186
    def set_program(self, program=0):
        self.program = program

    # 弹奏一个音符
    def play_note(self, note, length, delay=0, velocity=1.0, channel=0):
        meta_time = 60 * 60 * 10 / bpm #根据bpm而计算出的每个节拍的时间长度
        self.track.append(
            Message('note_on', note=note, 
                    velocity=round(64 * velocity),
                    time=int(round(delay * meta_time)), channel=channel))
        self.track.append(
            Message('note_off', note=note,
                    velocity=round(64 * velocity),
                    time=int(round(meta_time * length)), channel=channel))
    
    # 保存为midi文件
    def save_mid(self):
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        self.mid.save(os.path.join(self.save_path, self.name+'.mid'))


if __name__ == "__main__":
    transcriber = music_transcriber.MusicTranscriber(os.path.join(BASE_DIR,'record_wav','twinkle_short.wav'))
    notes, durations = transcriber.transcribe()
    durations = [i*3 for i in durations]
    melody = [tuple(i) for i in zip(notes,durations)]
    twinkle = Music(b,'twinkle_short')
    