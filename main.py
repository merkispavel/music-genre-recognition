import numpy as np
import sys
from scikits.audiolab import Sndfile
from sklearn import svm

genres = ['metal', 'pop', 'blues', 'classical', 'country', 'disco',
          'hiphop', 'jazz', 'reggae', 'rock']

NUMBER_OF_FRAMES = 661504
NUMBER_OF_SOUNDS = 100
NUMBER_OF_GENRES = 2

path_to_genres = '/home/pavel/university/coursework/genres/'

sound_extension = '.au'


# sound = Sndfile(pop_sound_path, 'r')

def make_sound_file_name(genre, sound_index):
    sound_number = str(sound_index)
    sound_number = '0' * (5 - len(sound_number)) + sound_number
    return genre + '.' + sound_number + sound_extension


def process_sound_file(file, genre_index, data, genre_results):
    print(file)
    sys.exit(0)
    data.append(file.read_frames(NUMBER_OF_FRAMES, dtype=np.float64))
    genre_results.append(-1 if genre_index == 0 else 1)


def train_model(sound_data, genre_results):
    clf = svm.SVC(gamma=0.00005, C=10.)
    clf.fit(sound_data, genre_results)
    return clf

print('Read data...')

sound_data = []
genre_results = []
for genre_index in range(NUMBER_OF_GENRES):
    genre = genres[genre_index]
    for sound_index in range(NUMBER_OF_SOUNDS // 4 * 3):
        sound_name = make_sound_file_name(genre, sound_index)
        sound_path = path_to_genres + genre + '/' + sound_name
        sound_file = Sndfile(sound_path, 'r')
        process_sound_file(sound_file, genre_index, sound_data, genre_results)

#sys.exit(0)
print('Model train started')
clf = train_model(sound_data, genre_results)
print('Model trained')
mistakes = [0, 0]
for genre_index in range(NUMBER_OF_GENRES):
    genre = genres[genre_index]
    for sound_index in range(NUMBER_OF_SOUNDS // 4 * 3, NUMBER_OF_SOUNDS):
        sound_name = make_sound_file_name(genre, sound_index)
        sound_path = path_to_genres + genre + '/' + sound_name
        sound_file = Sndfile(sound_path, 'r')
        predict_result = clf.predict([sound_file.read_frames(NUMBER_OF_FRAMES)])
        mistakes[genre_index] += int(predict_result != (-1 if genre_index == 0 else 1))
        #print('Predicted {}, actually {}'.format(predict_result, genre_index))
    print()
print(mistakes)




# data = sound.read_frames(661504)
# print(data)
