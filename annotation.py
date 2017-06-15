from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import pprint
import solr  # corresponds to solrpy
import numpy as np


class Annotation(object):

    max_group_length = 5

    def __init__(self, data, video_id, print_structure=False):
        """Return a new Annotation object."""

        self.video_id = video_id
        self.sentences = []
        self.senses = []

        wnl = WordNetLemmatizer()
        tokenizer = RegexpTokenizer(r'\w+')

        sentences_video = [a['caption'] for a in data['sentences'] if a['video_id'] == video_id]

        sentence_i = 0
        token_i = 0
        sense_i = 0

        for sentence in sentences_video:
            sentence_i += 1

            sentence_info = {'sentence': sentence, 'sentence_id': sentence_i}

            # text = word_tokenize(sentence)
            text = tokenizer.tokenize(sentence)
            text = [word for word in text if word not in stopwords.words('english')]

            tokens = []

            for word in text:
                token_i += 1
                token_senses = []
                if word == '(':
                    import ipdb; ipdb.set_trace()
                word_senses = self.get_relevant_senses(word.lower())
                word_senses += self.get_relevant_senses(wnl.lemmatize(word))
                for index, sense in enumerate(word_senses):
                    sense_i += 1
                    sense['sense_id'] = sense_i
                    token_senses.append(sense)
                    self.senses.append({'id': str(sentence_i) + '_' + str(token_i) + '_' + str(sense_i), 'sensembed': sense['sensembed']})
                tokens.append({'token': word, 'token_id': token_i, 'senses': token_senses})

            groups = []
            for group_length in range(2, self.max_group_length + 1):
                i = 0
                while i + group_length <= len(text):
                    group_text = text[i:i + group_length]
                    groups.append('_'.join([a.lower() for a in group_text]))
                    groups.append('_'.join([wnl.lemmatize(a) for a in group_text]))
                    i += 1

            for group in list(set(groups)):
                word_senses = self.get_relevant_senses(group)
                token_i += 1
                token_senses = []
                for index, sense in enumerate(word_senses):
                    sense_i += 1
                    sense['sense_id'] = sense_i
                    token_senses.append(sense)
                    self.senses.append({'id': str(sentence_i) + '_' + str(token_i) + '_' + str(sense_i), 'sensembed': sense['sensembed']})
                tokens.append({'token': group, 'token_id': token_i, 'senses': token_senses})

            sentence_info['tokens'] = tokens

            self.sentences.append(sentence_info)

        if print_structure:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.sentences)

    @staticmethod
    def get_relevant_senses(word):
        # Returns set of relevant senses as decsribed in section 3.1 of SensEmbed:
        # Leaning Sense Embeddings for Word and Relational Similarity

        s = solr.SolrConnection('http://localhost:8983/solr/sensembed_vectors')
        word_senses1 = s.query('sense:' + word + '_bn*')
        word_senses2 = s.query('sense:' + word)
        return word_senses1.results + word_senses2.results

    def get_sentence_tokens(self, sentence_id):
        """ returns a list of dictionaries containing 'sense', 'sense_id' and
        'senseembed' of the tokens of the sentence 'sentence_id'.
        """
        return self.sentences[sentence_id]

    def get_sentence_text(self, sentence_id):
        return self.sentences[sentence_id]['sentence']

    def get_sentence_embedding(self, sentence_id):
        """ returns the sum of the embeddings of all the possible senses of all
        the tokens of the sentence 'sentence_id'
        """
        embedding = []
        tokens = self.sentences[sentence_id]['tokens']
        for token in tokens:
            for sense in token['senses']:
                embedding = np.sum([embedding, sense['sensembed']], axis=0)
        return embedding

    def get_sentence_embedding_BFS(self, sentence_id):
        """ returns the sum of the embeddings of the first sense of all
        the tokens of the sentence 'sentence_id'
        TODO lpmayos: we supose the senses are ordered by importance in solr (extracted from sensembed)
        """
        embedding = []
        tokens = self.sentences[sentence_id]['tokens']
        for token in tokens:
            if len(token['senses']) > 0:
                embedding = np.sum([embedding, token['senses'][0]['sensembed']], axis=0)
        return embedding
