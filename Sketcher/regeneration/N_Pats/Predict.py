# import library
import gensim
from six.moves import cPickle

# load the model
d2v_model = gensim.models.doc2vec.Doc2Vec.load('./data/doc2vec.w2v')

sentences_vector = []

t = 500

for i in range(len(sentences)):
    if i % t == 0:
        print("sentence", i, ":", sentences[i])
        print("***")
    sent = sentences[i]
    sentences_vector.append(d2v_model.infer_vector(sent, alpha=0.001, min_alpha=0.001, steps=10000))

# save the sentences_vector
sentences_vector_file = os.path.join(save_dir, "sentences_vector_500_a001_ma001_s10000.pkl")
with open(os.path.join(sentences_vector_file), 'wb') as f:
    cPickle.dump((sentences_vector), f)