#!omlet: nvcr.io/nvidia/tensorflow:21.09-tf2-py3
import os

import tensorflow as tf

from models import Model
from datasets import CatsVsDogsDataset


def main():
    model = Model()

    # test_dataset = CatsVsDogsDataset(os.path.join(os.path.dirname(__file__), 'dataset', 'test_set', 'test_set'))
    train_dataset = CatsVsDogsDataset(os.path.join(os.path.dirname(__file__), 'dataset', 'training_set', 'training_set'))

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=[tf.keras.metrics.CategoricalAccuracy(),
                           tf.keras.metrics.CategoricalCrossentropy()])

    history = model.fit(train_dataset, epochs=1)
    print('history:', history.history)

    model.save(os.path.join(os.path.dirname(__file__), 'model.ckpt'))


if __name__ == "__main__":
    main()
