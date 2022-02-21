import os

import tensorflow as tf

from omlet.checkpoint import save


class OmletCheckpointCallback(tf.keras.callbacks.Callback):
    def __init__(self, per_episode: int):
        self._per_episode = per_episode

    def on_epoch_end(self, epoch, logs=None):
        if epoch % self._per_episode == 0:
            checkpoint_path = os.path.join(os.path.dirname(__file__), 'model.ckpt')
            save(self.model, checkpoint_path, episode=epoch)

    def on_train_end(self, logs=None):
        pass
