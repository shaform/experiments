"""
Sampled MNIST Experiments
"""

import numpy as np
import xgboost as xgb

from sacred import Experiment
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from tensorflow.examples.tutorials.mnist import input_data

from softmax import SoftmaxClassifier

ex = Experiment('mnist_sampled')


@ex.config
def my_config():
    sample_size = 500
    classifier = 'svc'


@ex.capture
def sample_data(X, y, sample_size, _rnd):
    indices = np.arange(X.shape[0])
    choice_indices = _rnd.choice(indices, sample_size)
    return X[choice_indices, :], y[choice_indices]


@ex.capture
def get_classifier(classifier):
    if classifier == 'svc':
        return LinearSVC()
    elif classifier == 'softmax':
        return SoftmaxClassifier()
    elif classifier == 'xgb':
        return xgb.XGBClassifier()
    else:
        return None


@ex.automain
def run_experiments(data_dir='MNIST_data'):
    mnist = input_data.read_data_sets(data_dir, one_hot=False)
    X_test = mnist.test.images
    y_test = mnist.test.labels

    X_train, y_train = sample_data(mnist.train.images, mnist.train.labels)

    clf = get_classifier()
    clf.fit(X_train, y_train)
    y_train_pred = clf.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)

    y_test_pred = clf.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    return {'train_accuracy': train_accuracy, 'test_accuracy': test_accuracy}
