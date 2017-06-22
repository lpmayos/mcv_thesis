import itertools
import solr  # corresponds to solrpy
import numpy as np
import config


def get_relevant_senses(word):
    # Returns set of relevant senses as described in section 3.1 of SensEmbed:
    # Leaning Sense Embeddings for Word and Relational Similarity

    s = solr.SolrConnection('http://localhost:8983/solr/sensembed_vectors')
    word_senses1 = s.query('sense:' + word + '_bn*')
    word_senses2 = s.query('sense:' + word)
    return word_senses1.results + word_senses2.results


def tanimoto_distance(w1, w2):
    """
    """
    return np.dot(w1, w2) / ((np.linalg.norm(w1, 2))**2 + (np.linalg.norm(w2, 2))**2 - np.dot(w1, w2))


def word_similarity_closest(token1, token2):
    """ implementation of the word similarity measure described in algorithm 1
    of senseEmbed paper using the 'closest' strategy
    TODO lpmayos: add 'weighted' strategy
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
