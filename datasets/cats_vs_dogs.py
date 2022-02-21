import os

import tensorflow as tf
import numpy as np
from PIL import Image


class Dataset(tf.keras.utils.Sequence):
    def __init__(self, root: str, batch_size=32, shuffle=False):
        cats = [(os.path.join(root, 'cats', path), 0) for path in os.listdir(os.path.join(root, 'cats'))]
        dogs = [(os.path.join(root, 'dogs', path), 1) for path in os.listdir(os.path.join(root, 'dogs'))]
        self._dataset = cats + dogs
        np.random.shuffle(self._dataset)
        self._batch_size = batch_size
        self._shuffle = shuffle
        self._cache_dir = os.path.join(root, '.cache')
        if not os.path.exists(self._cache_dir):
            os.mkdir(self._cache_dir)

    def __len__(self):
        value = np.ceil(len(self._dataset) / self.batch_size).astype(np.uint8)
        return value

    def __getitem__(self, index):
        batch = {'image': [], 'label': []}
        datasets = self._dataset[index*self.batch_size:(index+1)*self.batch_size]
        for path, label in datasets:
            cache = os.path.join(self._cache_dir, os.path.split(path)[-1] + '.npy')
            try:
                image = np.load(cache)
            except FileNotFoundError:
                image = Image.open(path)
                image = np.asarray(image)
                np.save(cache, image)
            image = tf.convert_to_tensor(image, dtype=tf.float32)
            image = tf.image.resize(image, (224, 224))
            label = tf.squeeze(tf.one_hot([label], 2, axis=1))
            label = tf.convert_to_tensor(label, dtype=tf.float32)
            batch['image'].append(image)
            batch['label'].append(label)
        return (
            tf.stack(batch['image'], axis=0),
            tf.stack(batch['label'], axis=0)
        )

    def on_epoch_end(self):
        if self._shuffle:
            np.random.shuffle(self._dataset)

    @property
    def batch_size(self):
        return self._batch_size
