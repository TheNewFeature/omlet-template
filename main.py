#!omlet: nvcr.io/nvidia/tensorflow:21.09-tf2-py3
import os

import tensorflow as tf

from models import Model
from datasets import CatsVsDogsDataset
from omlet.checkpoint import save_checkpoint
from omlet.dataset import download_dataset
from omlet.tensorflow.callbacks import OmletCheckpointCallback


def main():
    model = Model()

    dataset_dir = download_dataset()
    print('Dataset Dir:', dataset_dir)

    # test_dataset = CatsVsDogsDataset(os.path.join(dataset_dir, 'test_set', 'test_set'))
    train_dataset = CatsVsDogsDataset(os.path.join(dataset_dir, 'training_set', 'training_set'))

    callbacks = [
        OmletCheckpointCallback(per_episode=1)
    ]

    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.CategoricalCrossentropy(),
                  metrics=[tf.keras.metrics.CategoricalAccuracy(),
                           tf.keras.metrics.CategoricalCrossentropy()])

    epochs = 1
    history = model.fit(train_dataset, epochs=1)
    print('history:', history.history)

    checkpoint_path = os.path.join(os.path.dirname(__file__), 'model.ckpt')
    save_checkpoint(model, checkpoint_path, episode=epochs)


if __name__ == "__main__":
    main()
