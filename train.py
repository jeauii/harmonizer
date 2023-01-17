import sys
import numpy as np
import tensorflow as tf

from parse import SEQ_LEN

def main():
    data = np.load(sys.argv[2], allow_pickle=True)
    x = data['x']
    y = data['y']
    z = data['z']
    vocab = data['v']

    print(y.shape)
    try:
        model = tf.keras.models.load_model(sys.argv[1])
    except:
        model = tf.keras.models.Sequential([
            tf.keras.layers.Embedding(len(vocab), 8, input_length=SEQ_LEN, mask_zero=True),
            tf.keras.layers.LSTM(64, return_sequences=True),
            tf.keras.layers.LSTM(64),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(len(vocab), activation='softmax')
        ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'])

    model.fit(y, z, batch_size=32, epochs=int(sys.argv[3]))

    model.save(sys.argv[1])

if __name__ == '__main__':
    main()
