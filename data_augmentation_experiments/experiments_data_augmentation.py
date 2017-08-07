#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
import urllib

import itertools

import conll

import sys
sys.path.append("../")

import config
from commons import load_video_captions, add_training_sentences, create_training_sentences


EN_PARSER = "http://services-taln.s.upf.edu:8080/prod/transition-service/en/parse"


class TransitionClient(object):

    def __init__(self, parser_url):
        self.parser_url = parser_url

    def parse_text(self, text):

        try:
            params = u"text=%s" % (urllib.quote(text))
            request = urllib2.urlopen(self.parser_url, params)
        except:
            print '[ERROR] urllib had problems with ' + text + '. Skipped'
            return

        response = json.loads(request.read())

        if "error" in response:
            raise Exception(response["error"])

        return conll.ConllStruct(response["output"].encode('utf8'))


def prova():
    parser_en = TransitionClient(EN_PARSER)

    sentence = 'two men discuss education and philanthropy on a news program'
    sentence_conll = parser_en.parse_text(sentence)
    subject, predicate = sentence_conll.sentences[0].get_subject_and_predicate()
    print sentence
    print ' '.join([a.form for a in subject]) + ', ROOT: ' + [a.form for a in subject if a.subject_root][0]
    print ' '.join([a.form for a in predicate]) + ', ROOT: ' + [a.form for a in predicate if a.predicate_root][0] + '\n'


def compute_similarity(caption1_subject_tokens, caption2_subject_tokens):
    """ Based on experiments_ranking > experiment4
    """
    similarities = []
    for token1_id in caption1_subject_tokens:

        # find most similar token to sentence1.token1 in sentence2.tokens
        most_similar_token_in_sentence = (None, float('-inf'))
        for token2_id in caption2_subject_tokens:
            if (token1_id, token2_id) in config.tokens_set.tokens_similarities_closest:
                similarity = config.tokens_set.tokens_similarities_closest[(token1_id, token2_id)]
                if similarity > most_similar_token_in_sentence[1]:
                    most_similar_token_in_sentence = (token2_id, similarity)

        # store token similarity (depending on the experiments we check if it is over threshold)
        if most_similar_token_in_sentence[0] is not None:
            if most_similar_token_in_sentence[1] > 0.11:  # ranking exp > exp4 symmetrical th1
                similarities.append((most_similar_token_in_sentence[0], 1.0))  # for each token we add 1 instead of similarity
            else:
                similarities.append((None, 0))

    # compute and store similarity between sentence1 and sentence2
    if len(similarities) > 0:
        similarity = float(sum([a[1] for a in similarities])) / len(similarities)
    else:
        similarity = 0

    return similarity


def senses_match(caption1, caption2):
    """ If both subjects are talking about the same subject, both sentences are
    good pair to exchange subject and predicate.
    """
    tokens_caption1 = caption1['sentence'].tokens_id_list
    tokens_caption2 = caption2['sentence'].tokens_id_list

    caption1_subject_tokens = [a for a in tokens_caption1 if config.tokens_set.get_token_by_id(a).token in caption1['subject']['text']]
    caption2_subject_tokens = [a for a in tokens_caption2 if config.tokens_set.get_token_by_id(a).token in caption2['subject']['text']]

    similarity1 = compute_similarity(caption1_subject_tokens, caption2_subject_tokens)
    similarity2 = compute_similarity(caption2_subject_tokens, caption1_subject_tokens)
    similarity = (similarity1 + similarity2) / 2

    if similarity > 0.435:  # ranking exp > exp4 symmetrical th2
        # print caption1['subject']['text'] + ' ------ IS SIMILAR TO ------ ' + caption2['subject']['text'] + ' (' + str(similarity) + ')'
        return True
    # print caption1['subject']['text'] + ' ------ IS NOT SIMILAR TO ------ ' + caption2['subject']['text'] + ' (' + str(similarity) + ')'
    return False


def combine_subjects_and_predicates():
    """ generates new training sentences by replacing tokens with synonyms
        "done adding new training sentences! Added 450757 captions" (without subject sense matching)
        "done adding new training sentences! Added 283313 captions" (with subject sense matching)
        "done adding new training sentences! Added 408177 captions" (with subject sense matching over the previously cleaned training sentences)
    """
    parser_en = TransitionClient(EN_PARSER)
    videos_new_captions = {}

    data_file = open(config.path_to_train_val_videodatainfo)
    data = json.load(data_file)
    training_sentences = [a['caption'] for a in data['sentences']]

    for video_id in range(config.first_video, config.last_video):
        video_captions = load_video_captions(video_id)
        parsed_captions = []
        current_captions = []
        new_captions = []

        for i, sentence in enumerate(video_captions.sentences):

            # check that sentence was not discarded in the training set we are using (video_captions may not be updated)
            if sentence.sentence in training_sentences:

                # add original sentence to final sentences
                current_captions.append(sentence.sentence)

                sentence_conll = parser_en.parse_text(sentence.sentence)
                if sentence_conll:
                    try:
                        subject, predicate = sentence_conll.sentences[0].get_subject_and_predicate()
                        subj_singular = 'number=SG' in [a for a in subject if a.subject_root][0].pfeat
                        subject_text = ' '.join([a.form for a in subject])

                        # fix mistake when subject contains 'and' (i.e. A cat and a monkey are playing)
                        if ' and ' in subject_text:
                            subj_singular = False

                        predicate_singular = 'number=SG' in [a.feat for a in predicate if a.pos.startswith('VB')][0] and [a.form for a in predicate if a.pos.startswith('VB')][0] != 'are'

                        # don't consider sentences starting with 'there' as they are hard to combine (i.e. there is a dog sharing food with a cat)
                        if subject_text.lower() != 'there':
                            predicate_text = ' '.join([a.form for a in predicate])
                            subject = {'subject': subject, 'text': subject_text, 'singular': subj_singular}
                            predicate = {'predicate': predicate, 'text': predicate_text, 'singular': predicate_singular}
                            parsed_captions.append({'sentence': sentence, 'subject': subject, 'predicate': predicate})
                    except IndexError:
                        pass

        # print '\n@@@ Original sentences @@@'
        # for sentence in video_captions.sentences:
        #     print sentence.sentence

        # print '\n@@@ Combined sentences @@@'

        for caption in parsed_captions:
            # try to combine sentence subject with all other predicates
            subject = caption['subject']
            for caption2 in parsed_captions:
                number_matching = subject['singular'] == caption2['predicate']['singular']
                sense_matching = senses_match(caption, caption2)  # TODO lpmayos: put on True to execute first experiment

                candidate_caption = caption['subject']['text'] + ' ' + caption2['predicate']['text']
                if number_matching and sense_matching and candidate_caption not in current_captions:
                    new_captions.append(candidate_caption)

        # print '\n ------------------------------------------ video ' + str(video_id) + '\n'
        # for caption in list(set(new_captions)):
        #     print caption
        videos_new_captions[video_id] = list(set(new_captions + current_captions))

    create_training_sentences(videos_new_captions, config.path_to_new_train_val_videodatainfo)


def main():
    print '====================================== ' + config.options.experiment

    if config.options.experiment == 'combine_subjects_and_predicates':
        combine_subjects_and_predicates()
    else:
        print 'bye!'


# example call: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
