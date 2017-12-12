from scikits.audiolab import Sndfile
import os
import sys
import numpy as np


MUSIC_DIR = '/home/pavel/university/coursework/genres/'
SYMBOLS = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWX' + 'YZ1234567890'
STRINGS_FILE = '_strings_file'

INTERVAL_DUR = 0.5  # duration of song interval in seconds
NUM_OF_SUBINTERVALS = len(SYMBOLS)
SUBINTERVAL_LEN = 2. / NUM_OF_SUBINTERVALS


def get_index_by_mean(mean):
    return int((mean + 1) / SUBINTERVAL_LEN)

def convert_frames_to_symbol(frames):
    neg_frames = [frame for frame in frames if frame < 0]
    pos_frames = [frame for frame in frames if frame > 0]
    neg_mean = sum(neg_frames) / len(neg_frames)
    pos_mean = sum(pos_frames) / len(pos_frames)
    neg_index = get_index_by_mean(neg_mean)
    pos_index = get_index_by_mean(pos_mean)
    return SYMBOLS[neg_index] + SYMBOLS[pos_index]


def read_mono_frames(sound_file, nframes):
    return sound_file.read_frames(nframes).sum(axis=1) / 2


def convert_sound_to_string(sound_file):
    string_of_song = ''
    frames_per_interval = INTERVAL_DUR * sound_file.samplerate
    while True:
        try:
            frames = sound_file.read_frames(frames_per_interval)
        except RuntimeError:
            break
        symbol = convert_frames_to_symbol(frames)
        string_of_song += symbol
    return string_of_song


def get_mono_frames(sound_file):
    return sound_file.read_frames(sound_file.nframes).sum(axis=1) / 2


if __name__ == '__main__':
    genres = ['pop', 'metal']
    for genre in genres:
        count = 0
        genre_strings_list = []
        genre_dir = '{}{}/'.format(MUSIC_DIR, genre)
        for filename in os.listdir(genre_dir):
            print('{} : {}...'.format(count, filename))
            sound_file = Sndfile(genre_dir + filename, 'r')
            genre_strings_list.append(convert_sound_to_string(sound_file))
            count += 1
        with open(genre + STRINGS_FILE, 'w+') as f:
            f.write('\n'.join(genre_strings_list))
