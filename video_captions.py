from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import pprint
import solr  # corresponds to solrpy
from data_structures.sentence import Sentence
from data_structures.sense import Sense
from data_structures.token import Token


class VideoCaptions(object):

    max_group_length = 5

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

        wnl = WordNetLemmatizer()
        tokenizer = RegexpTokenizer(r'\w+')

        sentences_video = [a['caption'] for a in data['sentences'] if a['video_id'] == video_id]

        sentence_i = 0
        token_i = 0
        sense_i = 0

        for sentence in sentences_video:
            sentence_i += 1

            sentenceObj = Sentence(sentence, sentence_i, [])

            text = tokenizer.tokenize(sentence)
            text = [word for word in text if word not in stopwords.words('english')]

            for word in text:
                token_i += 1
                token_senses = []
                word_senses = self.get_relevant_senses(word.lower())
                word_senses += self.get_relevant_senses(wnl.lemmatize(word))
                for index, sense in enumerate(word_senses):
                    sense_i += 1
                    token_senses.append(Sense(sense['sense'], sense_i, sense['sensembed']))
                sentenceObj.addToken(Token(word, token_i, token_senses))

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
                    token_senses.append(Sense(sense['sense'], sense_i, sense['sensembed']))
                sentenceObj.addToken(Token(group, token_i, token_senses))

            self.sentences.append(sentenceObj)

        if print_structure:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.sentences)

    @staticmethod
    def get_relevant_senses(word):
        # Returns set of relevant senses as described in section 3.1 of SensEmbed:
        # Leaning Sense Embeddings for Word and Relational Similarity

        s = solr.SolrConnection('http://localhost:8983/solr/sensembed_vectors')
        word_senses1 = s.query('sense:' + word + '_bn*')
        word_senses2 = s.query('sense:' + word)
        return word_senses1.results + word_senses2.results

    def get_sentence_text(self, sentence_id):
        """ returns a string containing the sentence itself
        """
        return self.sentences[sentence_id].get_sentence()
