from pydub import AudioSegment
import os
import sys

MUSIC_DIR = '/home/pavel/Projects/PythonProjects/TrackDownloader/'
PROJECT_DIR = '/home/pavel/Projects/PythonProjects/CourseWork/'


def convert_mp3_to_wav(filename, new_filename):
    mp3_file = AudioSegment.from_mp3(filename)
    mp3_file.export(new_filename, format='wav')


genres = ['pop', 'metal']
for genre in genres[1:]:
    count = 0
    MP3_GENRE_DIR = MUSIC_DIR + genre + '/'
    WAV_GENRE_DIR = PROJECT_DIR + genre + '_wav/'
    for filename in os.listdir(MP3_GENRE_DIR):
        if not filename.endswith('.mp3'):
            continue
        print('{} : converting {}...'.format(count, filename))
        convert_mp3_to_wav(MP3_GENRE_DIR + filename, WAV_GENRE_DIR + filename[:-4] + '.wav')
        count += 1
        break

