import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

def load_data(path):
    df = pd.read_csv(path, sep="\t", header=None, names=["devanagari", "latin", "count"])
    return df.dropna()

def create_vocab(data):
    latin_chars = set(char for word in data["latin"] for char in word.lower())
    devanagari_chars = set(char for word in data["devanagari"] for char in word)
    
    special_tokens = ['<start>', '<end>', '<pad>', '<unk>']
    all_chars = sorted(latin_chars) + sorted(devanagari_chars) + special_tokens
    char_to_id = {char: i for i, char in enumerate(all_chars)}
    return char_to_id, len(all_chars)

def preprocess(data, char_to_id, max_length=20):
    data["latin_seq"] = data["latin"].apply(
        lambda x: [char_to_id[c] for c in x.lower()] + [char_to_id['<end>']]
    )
    data["devanagari_seq"] = data["devanagari"].apply(
        lambda x: [char_to_id['<start>']] + [char_to_id[c] for c in x] + [char_to_id['<end>']]
    )
    
    X = pad_sequences(data["latin_seq"], maxlen=max_length, padding="post", value=char_to_id['<pad>'])
    y = pad_sequences(data["devanagari_seq"], maxlen=max_length, padding="post", value=char_to_id['<pad>'])
    return X, y

if __name__ == "__main__":
    data = load_data("hi.translit.sampled.train.tsv")
    char_to_id, vocab_size = create_vocab(data)
    X_train, y_train = preprocess(data, char_to_id)
    
    np.save("X_train.npy", X_train)
    np.save("y_train.npy", y_train)
    np.save("char_to_id.npy", char_to_id)
    print("Preprocessing completed. Vocabulary size:", vocab_size)