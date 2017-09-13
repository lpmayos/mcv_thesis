#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
import urllib
import sys
from nltk.corpus import wordnet as wn
import pattern
from pattern.en import conjugate, PARTICIPLE, PAST, PRESENT, PLURAL, SINGULAR
sys.path.append("../")
sys.path.append("../experiments_data_augmentation")
import config
from commons import load_video_captions, add_training_sentences, create_training_sentences
from experiments_data_augmentation import TransitionClient, parse_captions


EN_PARSER = "http://services-taln.s.upf.edu:8080/prod/transition-service/en/parse"


# 'of$IN|NN$group|*'
# http://10.80.27.67/webservice/test_pmi?solr_url=http%3A%2F%2F10.80.27.67%3A8080%2Fsolr%2Fbnc%2F&base=group&base_pos=NN&collocative=people&collocative_pos=NN&base_preposition=of&lang=en
# http://10.80.27.67/webservice/test_pmi?solr_url=http%3A%2F%2F10.80.27.67%3A8080%2Fsolr%2Fbnc%2F&lang=en&base=group&base_pos=NN&collocative=people&collocative_pos=NN&base_preposition=of

def do_pmi(combination_words, context_words):

    # # TODO for tokens with multiple words, i.e. 'comic strip NN*', we keep first word, 'comic NN*' because the web service does not support multiwords yet
    # context_words = [a.split()[0] + ' ' + a.split()[-1] for a in context_words]
    # combination_words = [a.split()[0] + ' ' + a.split()[-1] for a in combination_words]

    solr_url = "http://10.80.27.67:8080/solr/bnc/"

    param_dict = {"solr_url": solr_url,
                  "combination_words": combination_words,
                  "context_words": context_words}

    params = urllib.urlencode(param_dict, True)
    request = urllib2.urlopen("http://10.80.27.67/webservice/test_context_pmi?" + params)

    response = json.loads(request.read())

    if "error" in response:
        raise Exception(response["error"])

    return response


def compute_similarity(caption1_subject_tokens, caption2_subject_tokens):
    """ Based on experiments_ranking > experiment4
    Copy of the function in experiments_data_augmentation.py, but adding
    similarity instead of 1 (because we want to find the closest group, and
    similarity between (u'a person', u'a car') was 1 otherwise)
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
                similarities.append(most_similar_token_in_sentence)  # changed line with respect to function in experiments_data_augmentation.py
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

    root_caption1 = ' '.join([a.form for a in caption1['subject']['subject'] if a.subject_root])
    root_caption2 = ' '.join([a.form for a in caption2['subject']['subject'] if a.subject_root])

    caption1_subject_tokens = [a for a in tokens_caption1 if config.tokens_set.get_token_by_id(a).token in root_caption1]
    caption2_subject_tokens = [a for a in tokens_caption2 if config.tokens_set.get_token_by_id(a).token in root_caption2]

    similarity1 = compute_similarity(caption1_subject_tokens, caption2_subject_tokens)
    similarity2 = compute_similarity(caption2_subject_tokens, caption1_subject_tokens)
    similarity = (similarity1 + similarity2) / 2

    # print root_caption1, root_caption2, similarity
    # cat dog 0.496842531883
    # man guy 0.196757692797
    # man man 1.0
    # men someone 0.0
    # men man 0.235960463174
    # woman person 0.33271940638
    # beatles man 0.0
    # ghost secret 0.237277743194
    # ghost guy 0.126937045444
    # ghost man 0.163853100341

    if similarity > 0.18:  # threshold determined manually by inspecting results
        return True, similarity
    return False, similarity


def create_groups(parsed_captions):
    """
    """
    groups = []  # [[1, 3, 4], [2, 5], ...]
    for i, caption1 in enumerate(parsed_captions):
        closest_group_id = None
        closest_group_similarity = float('-inf')

        for j, group in enumerate(groups):
            for caption_id in group:
                if i != caption_id:
                    caption2 = parsed_captions[caption_id]

                    number_matching = caption1['subject']['singular'] == caption2['subject']['singular']
                    sense_matching, similarity = senses_match(caption1, caption2)
                    if number_matching and sense_matching and similarity > closest_group_similarity:
                        closest_group_id = j
                        closest_group_similarity = similarity

        if closest_group_id is None:  # create new group
            groups.append([i])
        else:
            groups[closest_group_id].append(i)
    return groups


def find_candidates_and_contexts(group, parsed_captions):
    candidates = []  # contruct candidates with central element of subjects
    context = []  # construct context with relevant elements from predicates
    for caption_id in group:
        caption = parsed_captions[caption_id]
        subject = caption['subject']['subject']

        # # if the subject contains a group of NN + IN + NN, we use it instead of the subject root. i.e. "a group of people", we use 'group of people' instead of just 'group'
        # group_found = None
        root = [a for a in subject if a.subject_root][0]
        # prep = [a for a in root.children if 'spos' in a.pfeatures and a.pfeatures['spos'] == 'IN']
        # if prep:
        #     prep = prep[0]
        #     nn = [a for a in prep.children if 'spos' in a.pfeatures and a.pfeatures['spos'] == 'NN']
        #     if nn:
        #         nn = nn[0]
        #         start = int(root.features['start_string'])
        #         end = int(nn.features['end_string'])
        #         group_found = True
        #         pmi_array = ['%s$IN|NN$%s|' % (prep.lemma, root.lemma), nn.lemma + '%s$NN|IN$%s|' % (nn.lemma, prep.lemma)]  # [of$IN|NN$group|, people$NN|IN$of|]

        # if not group_found:
        #     start = int(root.features['start_string'])
        #     end = int(root.features['end_string'])
        #     pmi_array = [root.lemma + ' ' + root.pfeatures['spos']]

        start = int(root.features['start_string'])
        end = int(root.features['end_string'])
        pmi_array = [root.lemma + ' ' + root.pfeatures['spos']]

        new_candidate = {'subject_text': caption['subject']['text'],
                         'candidate': caption['sentence'].sentence[start:end],
                         'pmi_array': pmi_array,
                         'start': start,
                         'end': end,
                         'caption_id': caption_id}

        candidates.append(new_candidate)

        caption['predicate']['context'] = []  # for each predicate, save individual context (relevant elements from subjects and predicate, excluding verbs)
        predicate = caption['predicate']['predicate']
        for element in predicate:
            if element.pos.startswith('NN'):
                context.append(element.lemma + ' NN*')
                caption['predicate']['context'].append(element.lemma + ' NN*')
            elif element.pos.startswith('VB'):
                context.append(element.lemma + ' VB*')
            elif element.pos.startswith('JJ'):
                context.append(element.lemma + ' JJ*')
                caption['predicate']['context'].append(element.lemma + ' JJ*')

        for element in subject:
            if element.pos.startswith('NN'):
                caption['predicate']['context'].append(element.lemma + ' NN*')
            elif element.pos.startswith('JJ'):
                caption['predicate']['context'].append(element.lemma + ' JJ*')

    context = list(set(context))

    return candidates, context


def select_candidate(candidates, context):

    # find candidate with higher pmi
    pmi_dict = {}  # save coputed pmi's so we do not query twice for the same pmi!
    try:
        selected_candidate = None
        max_pmi = float('-inf')
        for candidate in candidates:
            if str(candidate['pmi_array']) in pmi_dict:
                pmi = pmi_dict[str(candidate['pmi_array'])]
            else:
                pmi = do_pmi(candidate['pmi_array'], context)
                pmi_dict[str(candidate['pmi_array'])] = pmi

            if pmi['normalized_pmi'] > max_pmi:
                max_pmi = pmi['normalized_pmi']
                selected_candidate = candidate

        # print 'from candidates @@@ ' + str(candidates) + ' @@@ and context @@@ ' + str(context) + ' @@@ we choose @@@ ' + str(selected_candidate) + ' @@@'
    except:
        # just in case the web service for do_pmi fails
        print '[ERROR] Something went wrong with do_pmi function. We choose first candidate of group.'
        selected_candidate = candidates[0]

    return selected_candidate


def association_strengthen():
    """ generates new training sentences by replacing those subjects with lower PMI with the ones with higher PMI,
    and replacing the verbs with the synset with higher PMI
    """

    synsets_dict = {}

    videos_new_captions = {}

    data_file = open(config.path_to_train_val_videodatainfo)
    data = json.load(data_file)

    training_sentences = {}
    for caption in data['sentences']:
        if caption['video_id'] in training_sentences:
            training_sentences[caption['video_id']].append(caption['caption'])
        else:
            training_sentences[caption['video_id']] = [caption['caption']]

    for video_id in range(config.first_video, config.last_video):
        print video_id

        video_captions = load_video_captions(video_id)
        parsed_captions, current_captions = parse_captions(video_captions, video_id, training_sentences)

        # create groups of captions whose subjects can be replaced by one of the subjects in the group (same number and meaning)
        groups = create_groups(parsed_captions)

        # for each group, find candidates and context, find candidate with higher pmi and replace candidates with higher-pmi candidate
        new_captions = []
        for i, group in enumerate(groups):

            # find candidates and context
            candidates_subject, context_predicates = find_candidates_and_contexts(group, parsed_captions)

            selected_candidate = select_candidate(candidates_subject, context_predicates)
            selected_candidate_offset = min([int(a.features['start_string']) for a in parsed_captions[selected_candidate['caption_id']]['subject']['subject']])
            selected_candidate_start = selected_candidate['start'] - selected_candidate_offset
            selected_candidate_end = selected_candidate['end'] - selected_candidate_offset
            selected_candidate_text = selected_candidate['subject_text'][selected_candidate_start:selected_candidate_end]

            for caption_id in group:

                caption = parsed_captions[caption_id]

                # replace candidates root with lower pmi with selected candidate
                subject_root = [a for a in caption['subject']['subject'] if a.subject_root]
                if len(subject_root) > 0 and selected_candidate_text not in caption['subject']['text']:
                    subject_root[0].form = selected_candidate_text
                subject = ' '.join([a.form for a in caption['subject']['subject']])

                # find verb synset with higher PMI and replace current verb
                # replaceable_verbs = []
                predicate_verbs = [a for a in caption['predicate']['predicate'] if a.pos.startswith('VB')]  # and a.predicate_root]
                for predicate_verb in predicate_verbs:
                    verb_lemma = predicate_verb.lemma

                    # save in dict because it takes long time to compute
                    if verb_lemma in synsets_dict:
                        verb_synsets_unique = synsets_dict[verb_lemma]
                    else:
                        verb_synsets = wn.synsets(verb_lemma, pos=wn.VERB)
                        if len(verb_synsets) > 0:
                            verb_synset = verb_synsets[0]
                            verb_synsets_unique = []
                            for lemma in verb_synset.lemma_names():
                                lemma_synsets = wn.synsets(lemma, pos=wn.VERB)
                                if len(lemma_synsets) > 0:
                                    verb_synsets_unique.append(lemma_synsets[0])
                            verb_synsets_unique = list(set(verb_synsets_unique))
                            synsets_dict[verb_lemma] = verb_synsets_unique

                    selected_verb = None
                    max_pmi = float('-inf')
                    for verb_synset in verb_synsets_unique:
                        try:
                            pmi = do_pmi([verb_synset.lemmas()[0].name() + ' VB'], caption['predicate']['context'])
                            if pmi['normalized_pmi'] > max_pmi:
                                max_pmi = pmi['normalized_pmi']
                                selected_verb = verb_synset
                        except:
                            print '[ERROR] Error in do_pmi, skipping verb_synset'

                    if selected_verb and selected_verb.lemma_names()[0] != verb_lemma:

                        new_verb = None

                        # properly conjugate the selected verb and replace it in caption['predicate']['text']
                        try:
                            if 'finiteness' in predicate_verb.features and predicate_verb.features['finiteness'] == 'PART':
                                new_verb = conjugate(selected_verb.lemma_names()[0], tense=(pattern.en.PAST + pattern.en.PARTICIPLE))
                            elif 'finiteness' in predicate_verb.features and predicate_verb.features['finiteness'] == 'GER':
                                new_verb = conjugate(selected_verb.lemma_names()[0], tense=pattern.text.GERUND)
                            elif 'tense' in predicate_verb.features and predicate_verb.features['tense'] == 'PAST':
                                new_verb = conjugate(selected_verb.lemma_names()[0], tense=PAST)
                            elif 'tense' in predicate_verb.features and predicate_verb.features['tense'] == 'PRES':
                                if 'person' in predicate_verb.features and predicate_verb.features['person'] == '3':
                                    new_verb = conjugate(selected_verb.lemma_names()[0], tense=PRESENT, number=SINGULAR)
                                else:
                                    new_verb = conjugate(selected_verb.lemma_names()[0], tense=PRESENT, number=PLURAL)
                        except KeyError, e:
                            print '[KeyError] I got a KeyError - reason "%s"' % str(e)
                            print predicate_verb.features

                        if new_verb:
                            predicate_verb.plemma = selected_verb.lemma_names()[0]
                            predicate_verb.form = new_verb
                            predicate_verb.lemma = selected_verb.lemma_names()[0]
                            predicate_verb.columns[1] = new_verb
                            predicate_verb.columns[2] = selected_verb.lemma_names()[0]
                            predicate_verb.columns[3] = selected_verb.lemma_names()[0]

                predicate = ' '.join([a.form for a in caption['predicate']['predicate']])
                new_captions.append(subject + ' ' + predicate)

        videos_new_captions[video_id] = list(set(new_captions))

        # original_sentences = training_sentences['video' + str(video_id)]
        # print '**************** Original sentences:**************************************'
        # for sentence in original_sentences:
        #     print '\t' + sentence

        # print '**************** New sentences:**************************************'
        # for sentence in new_captions:
        #     print '\t' + sentence

    create_training_sentences(videos_new_captions, config.path_to_new_train_val_videodatainfo)


def main():
    print '====================================== ' + config.options.experiment

    if config.options.experiment == 'association_strengthen':
        association_strengthen()
    else:
        print 'bye!'


# example call: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
