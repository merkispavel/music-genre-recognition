from converter import SYMBOLS
from scipy.sparse import csr_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn import svm
import numpy as np
import sys

def get_3gramm_index(substr):
    n = len(SYMBOLS)
    powers = [n * n, n, 1]
    index = 0
    for i, char in enumerate(substr):
        index += powers[i] * SYMBOLS.find(char)
    return index


def string_to_3gramm_map(string):
    map = {}
    n = len(string)
    for i in range(n - 2):
        substr = string[i:i + 3]
        if not map.get(substr):
            map[substr] = 0
        map[substr] += 1
    return map


def add_map_to_data(map, row, y):
    for substr, freq in map.items():
        substr_index = get_3gramm_index(substr)
        rows.append(row)
        columns.append(substr_index)
        frequences.append(freq)
        # X[row, substr_index] = int(freq)
    Y[row] = y



def process_pop_music():
    with open('pop_strings_file', 'r') as file:
        row = 100
        for line in file:
            map = string_to_3gramm_map(line)
            add_map_to_data(map, row, -1)
            row += 1


def process_metal_music():
    with open('metal_strings_file', 'r') as file:
        row = 0
        for line in file:
            map = string_to_3gramm_map(line)
            add_map_to_data(map, row, 1)
            row += 1




NUM_OF_SONGS = 200
num_of_substr_indexes = len(SYMBOLS) ** 3

rows = []
columns = []
frequences = []

# X = np.zeros((NUM_OF_SONGS, num_of_substr_indexes))
Y = np.zeros((NUM_OF_SONGS,))

process_metal_music()
process_pop_music()

X = csr_matrix((frequences, (rows, columns)), shape=(NUM_OF_SONGS, num_of_substr_indexes))


tries = 1000
mean_prec = mean_rec = mean_fbeta = 0.0
mean_roc_auc = 0.0
for i in range(tries):
    # print(i, '...')
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2)
    y_train = y_train.ravel()
    y_test = y_test.ravel()
    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
    y_predicted = clf.predict(X_test)
    mean_roc_auc += roc_auc_score(y_test, y_predicted)
    #print(clf.score(X_test, y_test))
    prec, rec, fbeta, supp = precision_recall_fscore_support(y_test, y_predicted)
    mean_prec += prec
    mean_rec += rec
    mean_fbeta += fbeta
#print(classification_report(y_test, y_predicted, target_names=['pop', 'metal']))
print('Precision {}, aver {}'.format(mean_prec / tries, sum(mean_prec / tries) / 2))
print('Recall {}, aver {}'.format(mean_rec / tries, sum(mean_rec / tries) / 2))
print('Fbeta {}, aver {}'.format(mean_fbeta / tries, sum(mean_fbeta / tries) / 2))
print('Roc-auc {}'.format(mean_roc_auc / tries))
