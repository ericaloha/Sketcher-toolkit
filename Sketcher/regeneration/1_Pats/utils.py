import numpy as np

def create_wordlist(doc):
    wl = []
    for word in doc:
        #if word.text not in ("\n","\n\n",'\u2009','\xa0'):
        wl.append(word.text.lower())
    return wl


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)