import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

from read_tab_files import TabFileReader


barb_forms = TabFileReader.tab_reader(
    "chl2024_barbacoandata/chl2023_barbacoan_forms.tab"
)

word_list = TabFileReader.get_word_list(barb_forms)

# convert words to character sequences
tokens = [list(word) for word in word_list]

# flatten the list of chars to fit LabelEncoder
flat_tokens = [item for sublist in tokens for item in sublist]

# encode characters as integers
encoder = LabelEncoder()
encoder.fit(flat_tokens)
encoded_tokens = [encoder.transform(word) for word in tokens]

# specify sequence length (how long each seq should be interpreted as)
sequence_length = 2

X = []
y = []

# go through each word and get every sequence with the seq len (hello > hel, ell, llo if seq_len = 3)
for seq in encoded_tokens:
    for i in range(sequence_length, len(seq)):
        X.append(seq[i - sequence_length : i])
        y.append(seq[i])


# prep data for training
X = np.array(X)
# reshape X to fit the LSTM input [samples, time steps, features]
X = np.reshape(X, (X.shape[0], X.shape[1], 1))
y = to_categorical(y)

model = Sequential(
    [
        # memory units (50 is good starting num), seq_len, step size (1)
        LSTM(50, input_shape=(X.shape[1], X.shape[2])),
        # num unique chars
        Dense(y.shape[1], activation="softmax"),
    ]
)

model.compile(loss="categorical_crossentropy", optimizer="adam")
model.fit(X, y, epochs=100, verbose=1)


def generate_word(model, input_text, extend_length, encoder):
    # pad text if its length is less than seq_len
    if len(input_text) < sequence_length:
        input_text = " " * (sequence_length - len(input_text)) + input_text

    for _ in range(extend_length):
        encoded = encoder.transform(list(input_text[-sequence_length:]))
        encoded = np.reshape(encoded, (1, sequence_length, 1))

        # predict next character
        pred = model.predict(encoded, verbose=0)
        next_char = encoder.inverse_transform([np.argmax(pred)])
        input_text += next_char[0]

    return input_text


new_word = generate_word(model, "puk", 5, encoder)
print("Generated word:", new_word)
