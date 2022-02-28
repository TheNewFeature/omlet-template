import os

import tensorflow as tf

from omlet.checkpoint import save_checkpoint


class OmletCheckpointCallback(tf.keras.callbacks.Callback):
    """`TensorFlow` Functional API의 `model.fit()`에서 `Checkpoint`를 저장하기 위한 콜백"""
    def __init__(self, per_episode: int):
        super(OmletCheckpointCallback, self).__init__()
        self._per_episode = per_episode

    def on_epoch_end(self, epoch, logs=None):
        if epoch % self._per_episode == 0:
            checkpoint_path = os.path.join(os.path.dirname(__file__), 'model.ckpt')
            save_checkpoint(self.model, checkpoint_path, episode=epoch)

    def on_train_end(self, logs=None):
        pass
