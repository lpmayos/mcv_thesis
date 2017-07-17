import json
import config
import numpy as np
import scipy
from commons import setup_logger, load_video_captions, plot_embeddings_with_labels, generate_barchart, generate_boxplot, remove_training_sentences
from data_structures.video_captions import VideoCaptions
import pickle
import logging


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
                pickle.dump(config.tokens_set, open('pickle_small/tokens_set_10.pickle', "wb"))
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

    Results:  a sample of the results can be seen at results/display_tokens_similarity/, and
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


def rank_captions_and_remove_worst_with_embeddings():
    """ experiment 1
    Goal: detect those captions that are very different from the others
    (they have typos or are not descriptive)

    Method: for each video we get all the captions and we compute an
    embedding for all the sentences. Then, we project all the embeddings
    in common space, we compute its centroid and the distances to the
    centroid of each embedding, sorting the captions by distance.
    Then, we discard the worst two annotations.
    TODO lpmayos: we can try discarding a percentage (i.e. 10%) or the ones that
    are above a certain threshold.

    Results: a sample of the results (sentence ordering and image of the
    embedding space) is shown on shell if verbose=True and can be also seen at
    results/experiment1/, and a new train_val_videodatainfo.json is generated to
    train a new model on config.path_to_train_val_videodatainfo with sufix
    # experiment1
    """

    # configure logging file
    setup_logger(config.experiment, config.log_path)
    log1 = logging.getLogger(config.experiment)

    bfs = True
    plot_embeddings = False
    sentences_to_remove = []
    all_videos_sentences_distances = []  # stores in a single array the distances computed for each video
    num_sentences_above_threshold = []

    for video_id in range(config.first_video, config.last_video):  # 0, 7010
        video_captions = load_video_captions(video_id)

        embeddings = []
        labels = []
        for sentence in video_captions.sentences:
            sentence_embedding = sentence.get_sentence_embedding(bfs)
            if len(sentence_embedding) > 0:  # there are sentences without senses (i.e. 'its a t') --> no embedding!
                embeddings.append(sentence_embedding)
                labels.append(sentence.sentence)

        embeddings_mean = np.mean(embeddings, axis=0)
        distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
        all_videos_sentences_distances += distances
        sort_index = np.argsort(distances)

        # compute how many sentences are above th2
        num_sentences_above_threshold_video = len([(video_captions.sentences[ind], video_id) for ind, a in enumerate(distances) if a > config.th2])
        num_sentences_above_threshold.append(num_sentences_above_threshold_video)

        to_remove = [(video_captions.sentences[ind], video_id) for ind, a in enumerate(distances) if a > config.th2]
        sentences_to_remove += to_remove

        if config.verbose:
            log1.info('\n\n ***** video ' + str(video_id) + '. Sentences from closest to fartest to the mean:\n')
            for index in sort_index:
                try:
                    log1.info('\t' + str(distances[index]) + ' \t ' + video_captions.get_sentence_text(index))
                except UnicodeEncodeError:
                    log1.info('\t [PRINTING ERROR] with printing sentence')

        if plot_embeddings:
            plot_embeddings_with_labels(embeddings, labels, 'sentence_embeddings_' + video_captions.video_id + '.png')

    generate_boxplot(all_videos_sentences_distances)
    generate_barchart(num_sentences_above_threshold)

    # generate a new training set removing the detected annotations
    remove_training_sentences(sentences_to_remove)


def rank_captions_and_remove_worst():
    """ experiments 2, 3 and 4
    """

    # configure logging file
    setup_logger(config.experiment, config.log_path)
    log = logging.getLogger(config.experiment)

    sentences_to_remove = []
    all_videos_sentences_similarities = []  # stores in a single array the similarities computed for each video
    num_sentences_below_threshold = []

    for video_id in range(config.first_video, config.last_video):
        video_captions = load_video_captions(video_id)

        result = np.zeros([20, 20])
        i = 0
        for sentence1 in video_captions.sentences:
            j = 0
            for sentence2 in video_captions.sentences:
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
                    # sentences_similarity = sum([a[1] for a in similarities]) / len(similarities)
                else:
                    sentences_similarity = 0

                result[i, j] = sentences_similarity

                if i != j:
                    all_videos_sentences_similarities.append(sentences_similarity)
                j += 1
            i += 1

        # we make the similarities symmetrical
        if config.experiment == 'experiment4symmetrical':
            all_videos_sentences_similarities = []
            for i in range(0, len(result)):
                for j in range(0, len(result)):
                    symmetric_similarity = 0
                    if result[i, j] + result[j, i] != 0:
                        symmetric_similarity = (result[i, j] + result[j, i]) / 2
                    result[i, j] = symmetric_similarity
                    result[j, i] = symmetric_similarity
                    all_videos_sentences_similarities += [symmetric_similarity, symmetric_similarity]

        # compute sentences similarity to all others (array of size 20)
        sentences_global_similarities = (np.sum(result, axis=1)) / result.shape[1]  # sentences similarities normalized between 0 and 1

        # compute sentences order according to similarity
        sentences_order = np.flip(np.argsort(sentences_global_similarities), 0)

        # show sentences and similarity from most similar to most different
        if config.verbose:
            log.info('\n\n ***** video ' + str(video_id) + '. Sentences from most similar to all others to most different to all others:\n')
            for sentence_index in sentences_order:
                try:
                    log.info('\t' + video_captions.sentences[sentence_index].sentence + ' (' + str(sentences_global_similarities[sentence_index]) + ')')
                except UnicodeEncodeError:
                    log.info('\t [PRINTING ERROR] with printing sentence')

        # compute which sentence we should remove according to similarity measures (or just the worst 2, depending on the policy)

        # compute how many sentences are below th2
        num_sentences_below_threshold_video = len([(video_captions.sentences[ind], video_id) for ind, a in enumerate(sentences_global_similarities) if a < config.th2])
        num_sentences_below_threshold.append(num_sentences_below_threshold_video)

        to_remove = [(video_captions.sentences[ind], video_id) for ind, a in enumerate(sentences_global_similarities) if a < config.th2]
        sentences_to_remove += to_remove

    # generate boxplots with sentences similarities and barchart of how many sentences we have to remove from each video according to threshold
    generate_boxplot(all_videos_sentences_similarities)
    generate_barchart(num_sentences_below_threshold)

    # generate a new training set removing the detected annotations
    remove_training_sentences(sentences_to_remove)

    # remove file handlers
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)


def main():
    print '====================================== ' + config.options.experiment

    if config.options.experiment == 'create_video_captions':
        create_video_captions()
    elif config.options.experiment == 'display_tokens_similarity':
        display_tokens_similarity()
    elif config.options.experiment == 'experiment1':
        rank_captions_and_remove_worst_with_embeddings()
    elif config.options.experiment in ['experiment2', 'experiment3', 'experiment4', 'experiment4symmetrical']:
        rank_captions_and_remove_worst()
    elif config.options.experiment == 'find_th1':
        for experiment_to_test in ['experiment4symmetrical']:  # ['experiment3', 'experiment4', 'experiment4symmetrical']:
            config.experiment = experiment_to_test
            for th1 in [0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30]:  # token similarity moves between 0 and 1
                config.th1, config.sufix_files, config.folder, config.boxplot_path, config.barchart_path, config.log_path = config.config_th1_and_paths(th1, config.th2, experiment_to_test)
                rank_captions_and_remove_worst()
    else:
        print 'bye!'


# example call: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
