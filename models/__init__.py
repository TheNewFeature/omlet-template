import tensorflow as tf


class Model(tf.keras.Model):
    def __init__(self, input_size=(224, 224, 3), output_size=2, hidden_size=256):
        super(Model, self).__init__()
        self.backbone = tf.keras.applications.vgg16.VGG16(include_top=False, weights='imagenet', input_shape=input_size)
        self.flatten = tf.keras.layers.Flatten()
        self.dense1 = tf.keras.layers.Dense(hidden_size, activation='relu')
        self.dense2 = tf.keras.layers.Dense(hidden_size, activation='relu')
        self.head = tf.keras.layers.Dense(output_size)

    def call(self, x):
        x = self.backbone(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)
        x = tf.nn.softmax(self.head(x))
        return x
