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


# def combine_subjects_and_predicates_OLD():
#     """ generates new training sentences by replacing tokens with synonyms
#     """
#     parser_en = TransitionClient(EN_PARSER)

#     for video_id in range(config.first_video, config.last_video):
#         video_captions = load_video_captions(video_id)
#         subjects = []
#         predicates = []
#         for i, sentence in enumerate(video_captions.sentences):
#             sentence_conll = parser_en.parse_text(sentence.sentence)
#             try:
#                 subject, predicate = sentence_conll.sentences[0].get_subject_and_predicate()
#                 # print sentence.sentence
#                 # print ' '.join([a.form for a in subject]) + ', ROOT: ' + [a.form for a in subject if a.subject_root][0]
#                 # print ' '.join([a.form for a in predicate]) + ', ROOT: ' + [a.form for a in predicate if a.predicate_root][0] + '\n'
#                 subj_singular = 'number=SG' in [a for a in subject if a.subject_root][0].pfeat
#                 subject_text = ' '.join([a.form for a in subject])
#                 predicate_text = ' '.join([a.form for a in predicate])
#                 if subject_text not in [subj['text'] for subj in subjects]:
#                     subjects.append({'subject': subject, 'text': subject_text, 'singular': subj_singular})
#                 if predicate_text not in [pred['text'] for pred in predicates]:
#                     predicates.append({'predicate': predicate, 'text': predicate_text, 'singular': subj_singular})  # NOTICE we mark predicate as singula or plural according to subject, not according to predicate because the model is noisy (i.e. classifies as plural 'are')
#             except IndexError:
#                 # print '\n[ERROR] Unable to extract subject/predicate from: ', sentence.sentence
#                 pass

#         print '\n ------------------------------------------ video ' + str(video_id)

#         print '\n@@@ Original sentences @@@'
#         for sentence in video_captions.sentences:
#             print sentence.sentence

#         print '\n@@@ Combined sentences @@@'
#         for subj_pred in list(itertools.product(subjects, predicates)):
#             subject = subj_pred[0]
#             predicate = subj_pred[1]
#             if subject['singular'] == predicate['singular']:
#                 sentence = ' '.join([a.form for a in subject['subject']]) + ' ' + ' '.join([a.form for a in predicate['predicate']])
#                 print sentence

#     # add_training_sentences(new_training_sentences, '/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo_synonyms.json')

def combine_subjects_and_predicates():
    """ generates new training sentences by replacing tokens with synonyms
    """
    parser_en = TransitionClient(EN_PARSER)

    for video_id in range(config.first_video, config.last_video):
        video_captions = load_video_captions(video_id)
        parsed_captions = []
        final_captions = []
        for i, sentence in enumerate(video_captions.sentences):

            # add original sentence to final sentences
            final_captions.append(sentence.sentence)

            sentence_conll = parser_en.parse_text(sentence.sentence)
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
                sense_matching = True  # TODO lpmayos xxx

                if number_matching and sense_matching:
                    final_captions.append(caption['subject']['text'] + ' ' + caption2['predicate']['text'])

        print '\n ------------------------------------------ video ' + str(video_id) + '\n'
        for caption in list(set(final_captions)):
            print caption

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
