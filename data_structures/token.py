class Token(object):

    def __init__(self, token, lemma, id, senses_list=[]):
        """
        """
        self.token = token
        self.lemma = lemma
        self.id = id
        self.senses = senses_list

    def add_sense(self, sense):
        self.senses.append(sense)

    # def set_similarity(self, token, similarity, token_similarities):
    #     token_similarities[(self.get_id(), token.get_id())] = similarity
    #     if token.sentence_id not in self.sentence_similarities or self.sentence_similarities[token.sentence_id][1] < similarity:
    #         self.sentence_similarities[token.sentence_id] = (token.get_id(), similarity)

    # def get_similarity(self, token, token_similarities):
    #     if (self.get_id(), token.get_id()) in token_similarities:
    #         return token_similarities[(self.get_id(), token.get_id())]
    #     else:
    #         return False

    # def get_most_similar_token(self, sentence_id):
    #     if sentence_id in self.sentence_similarities:
    #         return self.sentence_similarities[sentence_id]
