from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import pprint
from data_structures.sentence import Sentence
from data_structures.sense import Sense
from data_structures.token import Token
from commons import word_similarity_closest
from commons import get_relevant_senses


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
        self.similarities_computed = False

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
                word_senses = get_relevant_senses(word.lower())
                word_senses += get_relevant_senses(wnl.lemmatize(word))
                for index, sense in enumerate(word_senses):
                    sense_i += 1
                    token_senses.append(Sense(sense['sense'], str(sentence_i) + '_' + str(token_i) + '_' + str(sense_i), sense['sensembed']))
                if len(token_senses) > 0:
                    sentenceObj.add_token(Token(word, str(sentence_i) + '_' + str(token_i), token_senses))

            groups = []
            for group_length in range(2, self.max_group_length + 1):
                i = 0
                while i + group_length <= len(text):
                    group_text = text[i:i + group_length]
                    groups.append('_'.join([a.lower() for a in group_text]))
                    groups.append('_'.join([wnl.lemmatize(a) for a in group_text]))
                    i += 1

            for group in list(set(groups)):
                word_senses = get_relevant_senses(group)
                token_i += 1
                token_senses = []
                for index, sense in enumerate(word_senses):
                    sense_i += 1
                    token_senses.append(Sense(sense['sense'], str(sentence_i) + '_' + str(token_i) + '_' + str(sense_i), sense['sensembed']))
                if len(token_senses) > 0:
                    sentenceObj.add_token(Token(group, str(sentence_i) + '_' + str(token_i), token_senses))

            self.sentences.append(sentenceObj)

        if print_structure:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(self.sentences)

    def get_sentence_text(self, sentence_id):
        """ returns a string containing the sentence itself
        """
        return self.sentences[sentence_id].get_sentence()

    def compute_word_similarity(self):
        """
        """
        for sentence1 in self.sentences:
            for token1 in sentence1.get_tokens():
                for sentence2 in self.sentences:
                    if sentence1 != sentence2:
                        for token2 in sentence2.get_tokens():
                            similarity = word_similarity_closest(token1, token2)
                            token1.set_similarity(token2, similarity)

                            # for each token we need to save which token of each other sentence is most similar
                            token1.updateSimilarity(sentence2.get_id(), token2, similarity)

        self.similarities_computed = True
        return
