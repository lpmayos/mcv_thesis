import numpy as np


class Sentence(object):

    def __init__(self, sentence, id, tokens_id_list=[]):
        """
        """
        self.sentence = sentence
        self.id = id
        self.tokens_id_list = tokens_id_list

    def add_token(self, token_id):
        self.tokens_id_list.append(token_id)

    def get_sentence_embedding(self, tokens_set, bfs=True):
        """ if bfs, returns the sum of the embeddings of the first sense of all
        the tokens of the sentence 'sentence_id';
        else, returns the sum of the embeddings of all the possible senses of
        all the tokens of the sentence 'sentence_id'
        """
        embedding = []
        for token_id in self.tokens_id_list:
            token = tokens_set.get_token_by_id(token_id)
            if len(token.get_senses()) > 0:
                if bfs:
                    embedding = np.sum([embedding, token.get_senses()[0].get_sensembed()], axis=0)
                else:
                    for sense in token.get_senses():
                        embedding = np.sum([embedding, sense.get_sensembed()], axis=0)
        return embedding
