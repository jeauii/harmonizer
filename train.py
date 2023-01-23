import sys
import numpy as np
import tensorflow as tf

from parse import INPUT_LEN
from parse import VOCAB_PATH

def main():
    vocab = np.loadtxt(VOCAB_PATH, dtype=str)
    
    data = np.load(sys.argv[2])
    x = data['x']
    y = data['y']
    z = data['z']

    try:
        model = tf.keras.models.load_model(sys.argv[1])
    except:
        input1 = tf.keras.layers.Input(shape=(12))

        input2 = tf.keras.layers.Input(shape=(INPUT_LEN))
        embed = tf.keras.layers.Embedding(len(vocab), 8, mask_zero=True)(input2)
        lstm1 = tf.keras.layers.LSTM(64, return_sequences=True)(embed)
        lstm2 = tf.keras.layers.LSTM(64)(lstm1)

        concat = tf.keras.layers.Concatenate()([lstm2, input1])
        dense = tf.keras.layers.Dense(64, activation='relu')(concat)
        output = tf.keras.layers.Dense(len(vocab), activation='softmax')(dense)

        model = tf.keras.Model(inputs=[input1, input2], outputs=[output])

#        model = tf.keras.models.Sequential([
#            tf.keras.layers.Embedding(len(vocab), 8, input_length=SEQ_LEN, mask_zero=True),
#            tf.keras.layers.LSTM(64, return_sequences=True),
#            tf.keras.layers.LSTM(64),
#            tf.keras.layers.Dense(64, activation='relu'),
#            tf.keras.layers.Dense(len(vocab), activation='softmax')
#        ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['sparse_categorical_accuracy'])

    model.fit([x, y], z, batch_size=32, epochs=int(sys.argv[3]))

    model.save(sys.argv[1])

if __name__ == '__main__':
    main()
