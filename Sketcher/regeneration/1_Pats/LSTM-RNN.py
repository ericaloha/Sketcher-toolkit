'''
  #the whole process
    1.1 read the data (the novels we want to use),
    1.2 create the dictionnary of words,
    2. create the list of sentences,
    3. create the neural network,
    4. train the neural network,
    5. generate new sentences.
'''

# tensorfolw backend
from __future__ import print_function
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM, Input, Flatten, Bidirectional
# from keras.layers.normalization import BatchNormalization
from keras.layers import BatchNormalization
# from keras.optimizers import Adam
from tensorflow.keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.metrics import categorical_accuracy
import numpy as np
import os
import codecs
import collections
from six.moves import cPickle

# import spacy for preprocessing
# import spacy
from spacy.lang.fr import French

nlp = French()
print(111)
# nlp = spacy.load('fr')
# nlp = spacy.load('fr_core_news_sm')


'''
1. preprocessing
'''

# 1. local import
from utils import create_wordlist
from paras import rnn_size, learning_rate, batch_size, num_epochs, save_dir, file_list, data_dir, seq_length, \
    sequences_step

vocab_file = os.path.join(save_dir, "words_vocab.pkl")

# 2. create a list of sentence
wordlist = []

i=4
while i<=3:
    file_list.append(str(i))
    i+=1

for file_name in file_list:
    input_file = os.path.join(data_dir, file_name + ".txt")
    # read data
    with codecs.open(input_file, "r") as f:
        data = f.read()
    # create sentences
    doc = nlp(data)
    wl = create_wordlist(doc)
    wordlist = wordlist + wl

# 3. create the diretory

# count the number of words
word_counts = collections.Counter(wordlist)

# Mapping from index to word : that's the vocabulary
vocabulary_inv = [x[0] for x in word_counts.most_common()]
vocabulary_inv = list(sorted(vocabulary_inv))

# Mapping from word to index
vocab = {x: i for i, x in enumerate(vocabulary_inv)}
words = [x[0] for x in word_counts.most_common()]

# size of the vocabulary
vocab_size = len(words)
print("vocab size: ", vocab_size)

# save the words and vocabulary
with open(os.path.join(vocab_file), 'wb') as f:
    cPickle.dump((words, vocab, vocabulary_inv), f)

# 4.create sequences
sequences = []
next_words = []

for i in range(0, len(wordlist) - seq_length, sequences_step):
    sequences.append(wordlist[i: i + seq_length])
    next_words.append(wordlist[i + seq_length])

print('nb sequences:', len(sequences))

# 5.For each word, we retrieve its index in the vocabulary, and we set to 1 its position in the matrix.
X = np.zeros((len(sequences), seq_length, vocab_size), dtype=np.bool)
y = np.zeros((len(sequences), vocab_size), dtype=np.bool)
for i, sentence in enumerate(sequences):
    for t, word in enumerate(sentence):
        X[i, t, vocab[word]] = 1
    y[i, vocab[next_words[i]]] = 1

'''
    2. BUILD MODEL
    
'''
# 1. define model
def bidirectional_lstm_model(seq_length, vocab_size):
    print('Build LSTM model.')
    model = Sequential()
    model.add(Bidirectional(LSTM(rnn_size, activation="relu"), input_shape=(seq_length, vocab_size)))
    model.add(Dropout(0.6))
    model.add(Dense(vocab_size))
    model.add(Activation('softmax'))

    optimizer = Adam(lr=learning_rate)
    callbacks = [EarlyStopping(patience=2, monitor='val_loss')]
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=[categorical_accuracy])
    return model


# 2. invoke model
md = bidirectional_lstm_model(seq_length, vocab_size)
md.summary()

# 3.fit the model
callbacks = [EarlyStopping(patience=4, monitor='val_loss'),
             ModelCheckpoint(filepath=save_dir + "/" + 'my_model_gen_sentences_lstm.{epoch:02d}-{val_loss:.2f}.hdf5',
                             monitor='val_loss', verbose=0, mode='auto', period=2)]
history = md.fit(X, y,
                 batch_size=batch_size,
                 shuffle=True,
                 epochs=num_epochs,
                 callbacks=callbacks,
                 validation_split=0.01)

# 4. save the model
md.save(save_dir + "/" + 'my_model_gen_sentences_lstm.final.hdf5')
