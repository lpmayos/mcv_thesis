from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import pprint
from data_structures.sentence import Sentence
from data_structures.sense import Sense
from data_structures.token import Token
from commons import word_similarity_closest
from commons import get_relevant_senses
import itertools
import config


class VideoCaptions(object):

    max_group_length = 5
    wnl = WordNetLemmatizer()

    def __init__(self, data, video_id, print_structure=False):
        """ returns a new VideoCaptions object: a list of Sentences, one for
        each caption of the video with id 'video_id'.
        Each Sentence is composed of the text, an id and a list of Tokens, each
        of them composed by a token, an id and a list of Senses (sense, id and
        sensembed).
        See samples/video_captions_sample.txt to get an idea of the structure,
        even though is not a dictionary anymore (they are all objects).
        """

        self.video_id = video_id
        self.sentences = []
        self.num_senses = 0
        self.all_tokens = []

        tokenizer = RegexpTokenizer(r'\w+')

        sentences_video = [a['caption'] for a in data['sentences'] if a['video_id'] == video_id]

        sentence_i = 0

        for sentence in sentences_video:
            sentence_i += 1

            sentenceObj = Sentence(sentence, sentence_i, [])

            text = tokenizer.tokenize(sentence)
            text = [word for word in text if word not in stopwords.words('english')]

            for word in text:
                self.add_token(word, sentenceObj)

            groups = []
            for group_length in range(2, self.max_group_length + 1):
                i = 0
                while i + group_length <= len(text):
                    group_text = text[i:i + group_length]
                    groups.append('_'.join([a.lower() for a in group_text]))
                    groups.append('_'.join([self.wnl.lemmatize(a) for a in group_text]))
                    i += 1

            for group in list(set(groups)):
                self.add_token(group, sentenceObj)

            self.sentences.append(sentenceObj)

        if print_structure:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.sentences)

    def add_token(self, token_text, sentence):
        """
        """
        lemma = self.wnl.lemmatize(token_text)

        if lemma not in config.tokens_set.tokens_index_by_lemma:

            token_senses = []
            word_senses = get_relevant_senses(token_text.lower())
            word_senses += get_relevant_senses(self.wnl.lemmatize(token_text))
            for index, sense in enumerate(word_senses):
                self.num_senses += 1
                senseObj = Sense(sense['sense'], sense['sensembed'])
                token_senses.append(senseObj)

            # if it has senses, add token to config.tokens_set and add token_id to sentence tokens
            if len(token_senses) > 0:
                token_id = config.tokens_set.num_tokens
                token = Token(token_text, lemma, token_id, token_senses)
                config.tokens_set.add_token(token)

                sentence.add_token(token_id)
                self.all_tokens.append(token_id)
        else:
            # add token_id to sentence tokens
            token_id = config.tokens_set.get_token_id_by_lemma(lemma)
            sentence.add_token(token_id)
            self.all_tokens.append(token_id)

    def get_sentence_text(self, sentence_id):
        """ returns a string containing the sentence itself
        """
        return self.sentences[sentence_id].get_sentence()

    def compute_all_tokens_similarity(self):
        """
        """
        pairs = list(itertools.combinations(self.all_tokens, 2))
        print 'computing similarities for ' + str(len(pairs)) + ' pairs of tokens'
        for pair in pairs:
            token1 = config.tokens_set.tokens[pair[0]]
            token2 = config.tokens_set.tokens[pair[1]]
            similarity = word_similarity_closest(token1, token2)
            config.tokens_set.set_tokens_similarity_closest(pair[0], pair[1], similarity)
