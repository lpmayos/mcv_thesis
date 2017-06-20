import numpy as np


class Sentence(object):

    def __init__(self, sentence, id, tokens_list=[]):
        """
        """
        self.sentence = sentence
        self.id = id
        self.tokens = tokens_list

    def get_sentence(self):
        return self.sentence

    def get_id(self):
        return self.id

    def get_tokens(self):
        return self.tokens

    def set_tokens(self, tokens):
        self.tokens = tokens

    def add_token(self, token):
        self.tokens.append(token)

    def get_sentence_embedding(self, bfs=True):
        """ if bfs, returns the sum of the embeddings of the first sense of all
        the tokens of the sentence 'sentence_id';
        else, returns the sum of the embeddings of all the possible senses of
        all the tokens of the sentence 'sentence_id'
        """
        embedding = []
        for token in self.get_tokens():
            if len(token.get_senses()) > 0:
                if bfs:
                    embedding = np.sum([embedding, token.get_senses()[0].get_sensembed()], axis=0)
                else:
                    for sense in token.get_senses():
                        embedding = np.sum([embedding, sense.get_sensembed()], axis=0)
        return embedding
