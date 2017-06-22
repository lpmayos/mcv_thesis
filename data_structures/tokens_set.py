class TokensSet(object):

    def __init__(self):
        """
        """
        self.tokens = []  # a list of tokens appearing on all sentences, each id corresponding with the position in the list
        self.tokens_index_by_lemma = {}  # contains the positions in 'tokens' of tokens with lemma 'lemma'; i.e. {lemma: position, lemma, position}
        self.tokens_similarities_closest = {}  # i.e. {(token_id1, token_id2): similarity_a, (token_id1, token_id3): similarity_b, ...}
        self.num_tokens = 0

    def get_token_by_id(self, token_id):
        """
        """
        return self.tokens[token_id]

    def get_token_by_lemma(self, token_lemma):
        """
        """
        return self.tokens[self.tokens_index_by_lemma[token_lemma]]

    def get_token_id_by_lemma(self, token_lemma):
        """
        """
        token = self.get_token_by_lemma(token_lemma)
        return token.id

    def set_tokens_similarity_closest(self, token1_id, token2_id, similarity):
        """
        """
        self.tokens_similarities_closest[(token1_id, token2_id)] = similarity

    def add_token(self, token):
        """
        """
        self.tokens_index_by_lemma[token.lemma] = self.num_tokens
        self.tokens.append(token)
        self.num_tokens += 1
