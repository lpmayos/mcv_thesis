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
from commons import load_video_captions, add_training_sentences


EN_PARSER = "http://services-taln.s.upf.edu:8080/prod/transition-service/en/parse"


class TransitionClient(object):

    def __init__(self, parser_url):
        self.parser_url = parser_url

    def parse_text(self, text):

        params = u"text=%s" % (urllib.quote(text))
        request = urllib2.urlopen(self.parser_url, params)

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


def combine_subjects_and_predicates():
    """ generates new training sentences by replacing tokens with synonyms
    """
    parser_en = TransitionClient(EN_PARSER)

    for video_id in range(config.first_video, config.last_video):
        video_captions = load_video_captions(video_id)
        subjects = []
        predicates = []
        for i, sentence in enumerate(video_captions.sentences):
            sentence_conll = parser_en.parse_text(sentence.sentence)
            try:
                subject, predicate = sentence_conll.sentences[0].get_subject_and_predicate()
                # print sentence.sentence
                # print ' '.join([a.form for a in subject]) + ', ROOT: ' + [a.form for a in subject if a.subject_root][0]
                # print ' '.join([a.form for a in predicate]) + ', ROOT: ' + [a.form for a in predicate if a.predicate_root][0] + '\n'
                if ' '.join([a.form for a in subject]) not in [' '.join([b.form for b in subj]) for subj in subjects]:
                    subjects.append(subject)
                if ' '.join([a.form for a in predicate]) not in [' '.join([b.form for b in pred]) for pred in predicates]:
                    predicates.append(predicate)
            except IndexError:
                # print '\n[ERROR] Unable to extract subject/predicate from: ', sentence.sentence
                pass
        print '\n ------------------------------------------ video ' + str(video_id)
        for subj_pred in list(itertools.product(subjects, predicates)):
            subj_singular = 'number=SG' in [a for a in subj_pred[0] if a.subject_root][0].pfeat
            pred_singular = 'number=SG' in [a for a in subj_pred[1] if a.sentence_root][0].pfeat
            if subj_singular == pred_singular:
                print ' '.join([a.form for a in subj_pred[0]]) + ' ' + ' '.join([a.form for a in subj_pred[1]])

    # add_training_sentences(new_training_sentences, '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo_synonyms.json')


def main():
    print '====================================== ' + config.options.experiment

    if config.options.experiment == 'combine_subjects_and_predicates':
        combine_subjects_and_predicates()
    else:
        print 'bye!'


# example call: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
