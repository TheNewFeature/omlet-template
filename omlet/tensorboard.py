import os
from datetime import datetime

import numpy as np


def nsml_report(summary=False, scope=None, **kwargs):
    pass


def tensorflow_tensorboard():
    import tensorflow as tf

    current_time = datetime.now().strftime('%Y%m%d-%H%M%S')
    train_log_dir = os.path.join(os.path.dirname(__file__), 'logs', 'gradient_tape', current_time, 'train')
    train_summary_writer = tf.summary.create_file_writer(train_log_dir)

    for epoch in range(100):
        with train_summary_writer.as_default():
            tf.summary.scalar('loss', np.random.random(), step=epoch)
            tf.summary.scalar('accuracy', np.random.random(), step=epoch)


def pytorch_tensorboard():
    from torch.utils.tensorboard import SummaryWriter

    writer = SummaryWriter()
    for epoch in range(100):
        writer.add_scalar('Loss/train', np.random.random(), epoch)
        writer.add_scalar('Loss/test', np.random.random(), epoch)
        writer.add_scalar('Accuracy/train', np.random.random(), epoch)
        writer.add_scalar('Accuracy/test', np.random.random(), epoch)


def omlet_tensorboard():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
