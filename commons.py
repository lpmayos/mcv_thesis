import itertools
import numpy as np
import config
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pickle
import requests


def get_relevant_senses(word):
    # Returns set of relevant senses as described in section 3.1 of SensEmbed:
    # Leaning Sense Embeddings for Word and Relational Similarity

    word_senses1 = config.solr_connection.query('sense:' + word + '_bn*')
    word_senses2 = config.solr_connection.query('sense:' + word)
    return word_senses1.results + word_senses2.results


def tanimoto_distance(w1, w2):
    """
    """
    return np.dot(w1, w2) / ((np.linalg.norm(w1, 2))**2 + (np.linalg.norm(w2, 2))**2 - np.dot(w1, w2))


def word_similarity_closest(token1, token2):
    """ implementation of the word similarity measure described in algorithm 1
    of senseEmbed paper using the 'closest' strategy
    """
    if (token1.id, token2.id) in config.tokens_set.tokens_similarities_closest:
        similarity = config.tokens_set.tokens_similarities_closest[(token1.id, token2.id)]
    elif token1.id == token2.id:
        similarity = 1.0
    else:
        senses_combinations = list(itertools.product(token1.senses, token2.senses))
        similarity = -1
        for sense_combination in senses_combinations:
            similarity = max(similarity, tanimoto_distance(sense_combination[0].sensembed, sense_combination[1].sensembed))
    return similarity


def plot_embeddings_with_labels(embeddings, labels, filename='tsne.png'):

    # dimensionality reduction with PCA
    tsne = TSNE(perplexity=50, n_components=2, init='pca', n_iter=5000)
    low_dim_embs = tsne.fit_transform(embeddings)

    assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
    plt.figure(figsize=(18, 18))  # in inches
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        plt.scatter(x, y)
        plt.annotate(label,
                     xy=(x, y),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')

    plt.savefig(filename)


def load_video_captions(video_id):
    """
    """
    video_captions = pickle.load(open(config.pickle_folder + "/video_captions_" + str(video_id) + ".pickle", "rb"))
    return video_captions
