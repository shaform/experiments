"""
Softmax classifier implemented with TensorFlow
"""

import tensorflow as tf

from tensorflow.contrib import layers
from tensorflow.contrib.learn.python.learn.estimators import estimator
from tensorflow.contrib.learn.python.learn.estimators import model_fn


class SoftmaxClassifier(object):
    def __init__(self, output_dim=10):
        def softmax(features, target, mode):
            target = tf.one_hot(target, output_dim, 1, 0)
            logits = layers.fully_connected(
                inputs=features,
                num_outputs=output_dim,
                weights_initializer=tf.constant_initializer(0.),
                biases_initializer=tf.constant_initializer(0.),
                activation_fn=None)

            predictions = tf.argmax(tf.nn.softmax(logits), 1)
            loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(
                    labels=target, logits=logits))
            train_op = tf.contrib.layers.optimize_loss(
                loss,
                tf.contrib.framework.get_global_step(),
                optimizer='Adagrad',
                learning_rate=0.5)

            return model_fn.ModelFnOps(
                mode=mode,
                predictions=predictions,
                loss=loss,
                train_op=train_op)

        self.clf_ = estimator.SKCompat(estimator.Estimator(model_fn=softmax))

    def fit(self, X, y, steps=1000, batch_size=50):
        self.clf_.fit(X, y, steps=steps, batch_size=batch_size)
        return self

    def predict(self, X, batch_size=50):
        return self.clf_.predict(X, batch_size=batch_size)
