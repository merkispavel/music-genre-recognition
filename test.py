import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm

# iris = datasets.load_iris()
data = np.zeros((3, 3))
target = np.zeros((3, ))
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.4, random_state=0)


clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
print(clf.score(X_test, y_test))
