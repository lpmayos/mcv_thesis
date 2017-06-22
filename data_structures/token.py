class Token(object):

    def __init__(self, token, lemma, id, sentence_id, senses_list=[]):
        """
        """
        self.token = token
        self.lemma = lemma
        self.id = id
        self.senses = senses_list
        self.sentence_id = sentence_id
        self.token_similarities = {}
        self.sentence_similarities = {}

    def get_token(self):
        return self.token

    def get_lemma(self):
        return self.lemma

    def get_id(self):
        return self.id

    def get_senses(self):
        return self.senses

    def add_sense(self, sense):
        self.senses.append(sense)

    def set_similarity(self, token, similarity):
        self.token_similarities[token.get_id()] = similarity

        if token.sentence_id not in self.sentence_similarities or self.sentence_similarities[token.sentence_id].get_similarity(self) < similarity:
            self.sentence_similarities[token.sentence_id] = token

    def get_similarity(self, token):
        if token.get_id() in self.token_similarities:
            return self.token_similarities[token.get_id()]
        else:
            return False

    # def updateSimilarity(self, sentence_id, token, similarity):
    #     """ for each token we need to save which token of each other sentence is
    #     most similar
    #     """
    #     # if similarity between most similar token found up to now and self is smaller than new one
    #     if sentence_id not in self.sentence_similarities or self.sentence_similarities[sentence_id].get_similarity(self) < similarity:
    #         self.sentence_similarities[sentence_id] = token

    def get_most_similar_token(self, sentence_id):
        if sentence_id in self.sentence_similarities:
            return self.sentence_similarities[sentence_id]
