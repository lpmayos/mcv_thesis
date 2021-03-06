import sys
sys.path.append("../")

import json
import config
import numpy as np
import scipy
from commons import load_video_captions, generate_barchart, generate_boxplot, remove_training_sentences, log_sentences_ranking
from data_structures.video_captions import VideoCaptions
import pickle
from nltk.translate.bleu_score import SmoothingFunction
from nltk import bleu_score


def create_video_captions():
    """ Goal: create pickle files containing video and tokens information, to
    speed up the experiments.

    Method: for each video in train_val_set try to load videoCaption object
    from pickle. If it dies not exist, create a VideoCaption object and save it
    as pickle, and add all its tokens to token_set, containing information of
    all the tokens of all sentences of all videos.
    If compute_similarities is True, it computes the similarity between all
    pairs of tokens extracted from the annotations and saves it to tokens_set.

    Results: pickle files for each video and for tokens_set are saved to
    config.pickle_folder
    """
    with open(config.path_to_train_val_videodatainfo) as data_file:
        i = 0
        data = json.load(data_file)
        for video_id in range(config.first_video, config.last_video):

            try:
                video_captions = load_video_captions(video_id)
            except (OSError, IOError):
                print '*** creating pickle of video ' + str(video_id)
                video_captions = VideoCaptions(data, 'video' + str(video_id))
                pickle.dump(video_captions, open(config.pickle_folder + "/video_captions_" + str(video_id) + ".pickle", "wb"))

            video_captions.compute_all_tokens_similarity()

            i += 1
            if i == 10:
                print 'saving small tokens_set_10'
                pickle.dump(config.tokens_set, open('../pickle_small/tokens_set_10.pickle', "wb"))
            if i % 100 == 0:
                print 'iteration ' + str(i) + ' -----------> dumping tokens set'
                pickle.dump(config.tokens_set, open(config.tokens_set_to_load, "wb"))
        print 'iteration ' + str(i) + ' -----------> dumping tokens set'
        pickle.dump(config.tokens_set, open(config.tokens_set_to_load, "wb"))


def display_tokens_similarity():
    """ Goal: for each token of each sentence, computes which of the tokens of
    every other sentence is closer and shows it on shell.

    Method: in config.tokens_set we have computed the similarity of every pair
    of tokens, so we just loop over all of them and keep the most similar.

    Results:  a sample of the results can be seen at results_ranking/display_tokens_similarity/, and
    results are shown on shell
    """
    for video_id in range(config.first_video, config.last_video):
        print '\n\n ***** video ' + str(video_id)
        video_captions = load_video_captions(video_id)

        # for each token of each sentence we want to know wich token of every other sentence is closer
        for sentence1 in video_captions.sentences:
            try:
                print '\tsentence ' + str(sentence1.id) + ' ' + sentence1.sentence
            except UnicodeEncodeError:
                print '[PRINTING ERROR] with printing sentence ' + str(sentence1.id)
            for token1_id in sentence1.tokens_id_list:
                try:
                    print '\t\ttoken ' + config.tokens_set.tokens[token1_id].token
                except UnicodeEncodeError:
                    print '[PRINTING ERROR] with printing token'
                for sentence2 in video_captions.sentences:
                    most_similar_token_in_sentence = (None, float('-inf'))
                    for token2_id in sentence2.tokens_id_list:
                        if (token1_id, token2_id) in config.tokens_set.tokens_similarities_closest:
                            similarity = config.tokens_set.tokens_similarities_closest[(token1_id, token2_id)]
                            if similarity > most_similar_token_in_sentence[1]:
                                most_similar_token_in_sentence = (token2_id, similarity)
                    if most_similar_token_in_sentence[0] is not None:
                        try:
                            print '\t\t\tmost similar token in sentence ' + str(sentence2.id) + ' is ' + config.tokens_set.tokens[most_similar_token_in_sentence[0]].token + ' (' + str(most_similar_token_in_sentence[1]) + ')\t\t\t(' + sentence2.sentence + ')'
                        except UnicodeEncodeError:
                            print '\t\t\t[PRINTING ERROR] with printing most similar token in sentence ' + str(sentence2.id)


def compute_sentences_ranking(video_captions):
    """ returns [(sentence0, similarity), ..., (sentence19, similarity)]
    """
    sentences_global_ranking = []

    if config.experiment == 'experiment1':
        bfs = True
        embeddings = []
        labels = []
        for sentence in video_captions.sentences:
            sentence_embedding = sentence.get_sentence_embedding(bfs)
            if len(sentence_embedding) > 0:  # there are sentences without senses (i.e. 'its a t') --> no embedding!
                embeddings.append(sentence_embedding)
                labels.append(sentence.sentence)

        embeddings_mean = np.mean(embeddings, axis=0)
        distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
        for i, distance in enumerate(distances):
            sentences_global_ranking.append((video_captions.sentences[i].sentence, distance))

    elif config.experiment == 'experiment5':
        chencherry = SmoothingFunction()
        for i, sentence1 in enumerate(video_captions.sentences):
            scores = [bleu_score.sentence_bleu([sentence2.sentence.split(' ')], sentence1.sentence.split(' '), smoothing_function=chencherry.method4) for j, sentence2 in enumerate(video_captions.sentences)]  # if i != j]  # if we add 1 to all, result shouldn't change
            score = sum(scores) / len(scores)
            sentences_global_ranking.append((sentence1.sentence, score))

    else:
        result = np.zeros([20, 20])
        for i, sentence1 in enumerate(video_captions.sentences):
            for j, sentence2 in enumerate(video_captions.sentences):
                similarities = []
                for token1_id in sentence1.tokens_id_list:

                    # find most similar token to sentence1.token1 in sentence2.tokens
                    most_similar_token_in_sentence = (None, float('-inf'))
                    for token2_id in sentence2.tokens_id_list:
                        if (token1_id, token2_id) in config.tokens_set.tokens_similarities_closest:
                            similarity = config.tokens_set.tokens_similarities_closest[(token1_id, token2_id)]
                            if similarity > most_similar_token_in_sentence[1]:
                                most_similar_token_in_sentence = (token2_id, similarity)

                    # store token similarity (depending on the experiments we check if it is over threshold)
                    if most_similar_token_in_sentence[0] is not None:
                        if config.experiment in ['experiment4', 'experiment4symmetrical']:
                            if most_similar_token_in_sentence[1] > config.th1:
                                similarities.append((most_similar_token_in_sentence[0], 1.0))  # for each token we add 1 instead of similarity
                            else:
                                similarities.append((None, 0))
                        elif config.experiment == 'experiment3':
                            if most_similar_token_in_sentence[1] > config.th1:
                                similarities.append(most_similar_token_in_sentence)
                            else:
                                similarities.append((None, 0))
                        elif config.experiment == 'experiment2':
                            similarities.append(most_similar_token_in_sentence)

                # compute and store similarity between sentence1 and sentence2
                if len(similarities) > 0:
                    sentences_similarity = float(sum([a[1] for a in similarities])) / len(similarities)
                else:
                    sentences_similarity = 0

                result[i, j] = sentences_similarity

        # we make the similarities symmetrical
        if config.experiment == 'experiment4symmetrical':
            for i in range(0, len(result)):
                for j in range(0, len(result)):
                    symmetric_similarity = 0
                    if result[i, j] + result[j, i] != 0:
                        symmetric_similarity = (result[i, j] + result[j, i]) / 2
                    result[i, j] = symmetric_similarity
                    result[j, i] = symmetric_similarity

        # compute sentences similarity to all others (array of size 20)
        sentences_similarities = (np.sum(result, axis=1)) / result.shape[1]  # sentences similarities normalized between 0 and 1
        for i, similarity in enumerate(sentences_similarities):
            sentences_global_ranking.append((video_captions.sentences[i].sentence, similarity))

    return sentences_global_ranking


def rank_captions_and_remove_worst(similarity_or_distance='similarity'):
    """ experiments 1, 2, 3, 4, 4symmetrical and 5
    """

    video_captions_ranking = {}  # dict with the form {video_id: [(sentence0, similarity), ..., (sentence19, similarity)], ...} where similarity indicates how similar the caption is to all other captions of the same video

    for video_id in range(config.first_video, config.last_video):
        video_captions = load_video_captions(video_id)
        video_captions_ranking[video_id] = compute_sentences_ranking(video_captions)

    # log sentences ranking
    log_sentences_ranking(video_captions_ranking, similarity_or_distance)

    # generate boxplot with sentences similarities and compute th2
    th2 = generate_boxplot(video_captions_ranking, similarity_or_distance)

    # generate barchart of how many sentences we have to remove from each video according to threshold th2
    generate_barchart(video_captions_ranking, th2, similarity_or_distance)

    # generate a new training set removing the detected annotations
    remove_training_sentences(video_captions_ranking, th2, similarity_or_distance)


def main():
    print '====================================== ' + config.options.experiment

    if config.options.experiment == 'create_video_captions':
        create_video_captions()
    elif config.options.experiment == 'display_tokens_similarity':
        display_tokens_similarity()
    elif config.options.experiment == 'experiment1':
        rank_captions_and_remove_worst(similarity_or_distance='distance')
    elif config.options.experiment in ['experiment2', 'experiment3', 'experiment4', 'experiment4symmetrical', 'experiment5']:
        rank_captions_and_remove_worst()
    elif config.options.experiment == 'all':

        # # experiment 1
        # config.experiment, config.th1, config.th2, config.sufix_files, config.folder, config.boxplot_path, config.barchart_path, config.log_path = config.config_ths_and_paths(config.th1, config.th2, 'experiment1')
        # rank_captions_and_remove_worst(similarity_or_distance='distance')

        # experiment 4 and 4 symmetrical
        for experiment_to_test in ['experiment4', 'experiment4symmetrical']:  # ['experiment3', 'experiment4', 'experiment4symmetrical']:
            for th1 in [0.10]:  # [0.08, 0.085, 0.09, 0.095, 0.10, 0.11, 0.115, 0.12, 0.125, 0.13, 0.135]:  # token similarity moves between 0 and 1
                config.experiment, config.th1, config.th2, config.sufix_files, config.folder, config.boxplot_path, config.barchart_path, config.log_path = config.config_ths_and_paths(th1, config.th2, experiment_to_test)
                rank_captions_and_remove_worst()

        # # experiment 5
        # config.experiment, config.th1, config.th2, config.sufix_files, config.folder, config.boxplot_path, config.barchart_path, config.log_path = config.config_ths_and_paths(config.th1, config.th2, 'experiment5')
        # rank_captions_and_remove_worst()

    else:
        print 'bye!'


# example call: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
