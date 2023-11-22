import os
from six.moves import cPickle
from keras.models import load_model
import numpy as np

# 1. load vocabulary
from paras import save_dir, seq_length
from utils import sample

print("loading vocabulary...")
vocab_file = os.path.join(save_dir, "words_vocab.pkl")

with open(os.path.join(save_dir, 'words_vocab.pkl'), 'rb') as f:
    words, vocab, vocabulary_inv = cPickle.load(f)

vocab_size = len(words)

# 2. load the model
print("loading model...")
model = load_model(save_dir + "/" + 'my_model_gen_sentences_lstm.final.hdf5')

# 3.initiate sentences
seed_sentences = "start D_1_0_S22 D_1_1_S31 D_4_1_S36 D_5_0_S31 D_0_0_S35 D_0_0_S25 D_4_1_S31 D_3_0_S32 D_1_0_S35 D_5_2_S27 D_4_2_S25 end"
generated = ''
sentence = []
for i in range(seq_length):
    sentence.append("start")

seed = seed_sentences.split()

for i in range(len(seed)):
    sentence[seq_length - i - 1] = seed[len(seed) - i - 1]

generated += ' '.join(sentence)
print('Generating text with the following seed: "' + ' '.join(sentence) + '"')

print()

# 4.
words_number = 1000
# generate the text
for i in range(words_number):
    # create the vector
    x = np.zeros((1, seq_length, vocab_size))
    for t, word in enumerate(sentence):
        ww = word.lower()
        ss = vocab[word.lower()]
        #x[0, t, vocab[word]] = 1.
        x[0, t, ss] = 1.
    # print(x.shape)

    # calculate next word
    preds = model.predict(x, verbose=0)[0]
    next_index = sample(preds, 0.34)
    next_word = vocabulary_inv[next_index]

    # add the next word to the text
    generated += " " + next_word
    # shift the sentence by one, and and the next word at its end
    sentence = sentence[1:] + [next_word]

print(generated)
