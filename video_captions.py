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


class VideoCaptions(object):

    max_group_length = 5
    wnl = WordNetLemmatizer()

    def __init__(self, data, video_id, print_structure=False):
        """ returns a new VideoAnnotations object: a list of Sentences, one for
        each caption of the video with id 'video_id'.
        Each Sentence is composed of the text, an id and a list of Tokens, each
        of them composed by a token, an id and a list of Senses (sense, id and
        sensembed).
        See samples/video_captions_sample.txt to get an idea of the structure,
        even though is not a dictionary anymore (they are all objects).
        """

        self.video_id = video_id
        self.sentences = []
        self.all_tokens = []
        self.tokens_index = {}  # i.e. stores in which index of all_tokens is stored the token with key 'man'
        self.similarities_computed = False
        self.num_senses = 0

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

        if lemma in self.tokens_index:
            sentence.add_token(self.tokens_index[lemma])
        else:
            token_i = len(self.all_tokens)
            token_senses = []
            word_senses = get_relevant_senses(token_text.lower())
            word_senses += get_relevant_senses(self.wnl.lemmatize(token_text))
            for index, sense in enumerate(word_senses):
                self.num_senses += 1
                token_senses.append(Sense(sense['sense'], str(sentence.get_id()) + '_' + str(token_i) + '_' + str(self.num_senses), sense['sensembed']))
            if len(token_senses) > 0:
                self.tokens_index[lemma] = token_i
                token = Token(token_text, lemma, str(sentence.get_id()) + '_' + str(token_i), sentence.get_id(), token_senses)
                sentence.add_token(token_i)
                self.all_tokens.append(token)

    def get_sentence_text(self, sentence_id):
        """ returns a string containing the sentence itself
        """
        return self.sentences[sentence_id].get_sentence()

    def compute_word_similarity(self):
        """
        """
        pairs = list(itertools.combinations(self.all_tokens, 2))
        print 'computing similarities for ' + str(len(pairs)) + ' pairs of tokens'
        for pair in pairs:
            token1 = pair[0]
            token2 = pair[1]
            if token1.sentence_id != token2.sentence_id:
                similarity = word_similarity_closest(token1, token2)
                token1.set_similarity(token2, similarity)
                token2.set_similarity(token1, similarity)

        self.similarities_computed = True
