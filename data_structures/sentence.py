import numpy as np
import config


class Sentence(object):

    def __init__(self, sentence, id, tokens_id_list=[]):
        """
        """
        self.sentence = sentence
        self.id = id
        self.tokens_id_list = tokens_id_list

    def add_token(self, token_id):
        self.tokens_id_list.append(token_id)

    def get_sentence_embedding(self, bfs=True):
        """ if bfs, returns the sum of the embeddings of the first sense of all
        the tokens of the sentence 'sentence_id';
        else, returns the sum of the embeddings of all the possible senses of
        all the tokens of the sentence 'sentence_id'
        """
        embedding = []
        for token_id in self.tokens_id_list:
            token = config.tokens_set.get_token_by_id(token_id)
            if len(token.senses) > 0:
                if bfs:
                    embedding = np.sum([embedding, token.senses[0].sensembed], axis=0)
                else:
                    for sense in token.senses:
                        embedding = np.sum([embedding, sense.sensembed], axis=0)
        return embedding
