import json
import config
import numpy as np
import scipy
from commons import load_video_captions, plot_embeddings_with_labels
from data_structures.video_captions import VideoCaptions
import pickle


def remove_training_sentences(sentences_to_remove, new_file_appendix):
    """ Load the video annotations from json file, and makes a copy removing the
    sentences indicated in sentences_to_remove, adding a sufix to the file name.
    """
    with open(config.path_to_train_val_videodatainfo) as data_file:
        data = json.load(data_file)
        data_positions_to_remove = []
        for sentence_to_remove in sentences_to_remove:
            data_position = [i for i, a in enumerate(data['sentences']) if a['caption'] == sentence_to_remove[0].sentence and a['video_id'] == 'video' + str(sentence_to_remove[1])]
            data_positions_to_remove.append(data_position[0])
    new_data_sentences = [a for i, a in enumerate(data['sentences']) if i not in data_positions_to_remove]

    data['sentences'] = new_data_sentences

    new_file_path = config.path_to_train_val_videodatainfo.split('.json')[0] + '_' + new_file_appendix + '.json'
    with open(new_file_path, 'w') as outfile:
        json.dump(data, outfile)
    return


def experiment1(video_id_init, video_id_end):
    """ Goal: detect those captions that are wrong: they have typos or are
    not descriptive.

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
    bfs = True
    plot_embeddings = False
    sentences_to_remove = []
    for video_id in range(video_id_init, video_id_end):  # 0, 7010
        video_captions = load_video_captions(video_id)

        embeddings = []
        labels = []
        for sentence in video_captions.sentences:
            embeddings.append(sentence.get_sentence_embedding(bfs))
            labels.append(sentence.sentence)

        embeddings_mean = np.mean(embeddings, axis=0)
        distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
        sort_index = np.argsort(distances)

        for sentence_index in sort_index[18:]:  # we remove the two worst sentences
            sentences_to_remove.append((video_captions.sentences[sentence_index], video_id))

        if config.verbose:
            print '\n\n ***** video ' + str(video_id) + '. Sentences from closest to fartest to the mean:\n'
            for index in sort_index:
                print '\t' + str(distances[index]) + ' \t ' + video_captions.get_sentence_text(index)

        if plot_embeddings:
            plot_embeddings_with_labels(embeddings, labels, 'sentence_embeddings_' + video_captions.video_id + '.png')

    if config.pickle_folder == 'pickle' and video_id_init == 0 and video_id_end == 7010:
        remove_training_sentences(sentences_to_remove, 'experiment1')
    else:
        print '[WARNING] New json file not created because we are not working with the full data'


def experiment2(video_id_init, video_id_end):
    """ Goal: for each token of each sentence, computes which of the tokens of
    every other sentence is closer and shows it on shell.

    Method: in config.tokens_set we have computed the similarity of every pair
    of tokens, so we just loop over all of them and keep the most similar.

    Results:  a sample of the results can be seen at results/experiment2/, and
    results are shown on shell
    """
    for video_id in range(video_id_init, video_id_end):
        video_captions = load_video_captions(video_id)

        # for each token of each sentence we want to know wich token of every other sentence is closer
        for sentence1 in video_captions.sentences:
            print 'sentence ' + str(sentence1.id) + ' ' + sentence1.sentence
            for token1_id in sentence1.tokens_id_list:
                print '\ttoken ' + config.tokens_set.tokens[token1_id].token
                for sentence2 in video_captions.sentences:
                    most_similar_token_in_sentence = (None, float('-inf'))
                    for token2_id in sentence2.tokens_id_list:
                        if (token1_id, token2_id) in config.tokens_set.tokens_similarities_closest:
                            similarity = config.tokens_set.tokens_similarities_closest[(token1_id, token2_id)]
                            if similarity > most_similar_token_in_sentence[1]:
                                most_similar_token_in_sentence = (token2_id, similarity)
                    if most_similar_token_in_sentence[0] is not None:
                        print '\t\tmost similar token in sentence ' + str(sentence2.id) + ' is ' + config.tokens_set.tokens[most_similar_token_in_sentence[0]].token + ' (' + str(most_similar_token_in_sentence[1]) + ')\t\t\t(' + sentence2.sentence + ')'


def experiment3(video_id_init, video_id_end):
    """ Goal: compute sentences similarity and rank them.

    Method: for each pair of sentences, compute their similarity (non-symmetric)
    as the sum of the distances of each token in one sentence to the closest one
    in the other sentence, dividing by the number of tokens added. Then, discard
    the worst two annotations.
    TODO lpmayos: we can try discarding a percentage (i.e. 10%) or the ones that
    are above a certain threshold.

    Results: sentence ranking is shown on shell if verbose=True, a sample can be
    also seen at results/experiment3/, and a new train_val_videodatainfo.json is
    generated to train a new model on config.path_to_train_val_videodatainfo
    with sufix _experiment3
    """
    sentences_to_remove = []
    for video_id in range(video_id_init, video_id_end):
        video_captions = load_video_captions(video_id)

        result = np.empty([20, 20])
        i = 0
        for sentence1 in video_captions.sentences:
            j = 0
            for sentence2 in video_captions.sentences:
                similarities = []
                for token1_id in sentence1.tokens_id_list:
                    most_similar_token_in_sentence = (None, float('-inf'))
                    for token2_id in sentence2.tokens_id_list:
                        if (token1_id, token2_id) in config.tokens_set.tokens_similarities_closest:
                            similarity = config.tokens_set.tokens_similarities_closest[(token1_id, token2_id)]
                            if similarity > most_similar_token_in_sentence[1]:
                                most_similar_token_in_sentence = (token2_id, similarity)
                    if most_similar_token_in_sentence[0] is not None:
                        similarities.append(most_similar_token_in_sentence)
                if len(similarities) > 0:
                    sentences_similarity = sum([a[0] for a in similarities]) / len(similarities)
                else:
                    sentences_similarity = 0
                result[i, j] = sentences_similarity
                j += 1
            i += 1

        sentences_global_similarities = np.sum(result, axis=1)
        sentences_order = np.flip(np.argsort(sentences_global_similarities), 0)

        if config.verbose:
            print '\n\n ***** video ' + str(video_id) + '. Sentences from most similar to all others to most different to all others:\n'
            for sentence_index in sentences_order:
                print '\t' + video_captions.sentences[sentence_index].sentence + ' (' + str(sentences_global_similarities[sentence_index]) + ')'

        for sentence_index in sentences_order[18:]:  # we remove the two worst sentences
            sentences_to_remove.append((video_captions.sentences[sentence_index], video_id))

    if config.pickle_folder == 'pickle' and video_id_init == 0 and video_id_end == 7010:
        remove_training_sentences(sentences_to_remove, 'experiment3')
    else:
        print '[WARNING] New json file not created because we are not working with the full data'


def create_video_captions(video_id_init, video_id_end, compute_similarities=False):
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
        for video_id in range(video_id_init, video_id_end):

            try:
                video_captions = load_video_captions(video_id)
            except (OSError, IOError):
                print '*** creating pickle of video ' + str(video_id)
                video_captions = VideoCaptions(data, 'video' + str(video_id))
                pickle.dump(video_captions, open(config.pickle_folder + "/video_captions_" + str(video_id) + ".pickle", "wb"))

            if compute_similarities:
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


def compute_similarities(video_id_init, video_id_end):
    """ Compute the similarity between all pairs of tokens extracted from the
    annotations and save it to tokens_set, creating videoCaption objects for
    videos and saving them as pickle if they don't exist.
    TODO lpmayos: we'll have to refactor when we incorporate new siilarity
    strategies.
    """
    create_video_captions(video_id_init, video_id_end, True)


def main():
    first_video = int(config.options.first)
    last_video = int(config.options.last)

    if config.options.experiment == 'experiment1':
        print '====================================== experiment1'
        experiment1(first_video, last_video)
    elif config.options.experiment == 'experiment2':
        print '====================================== experiment2'
        experiment2(first_video, last_video)
    elif config.options.experiment == 'experiment3':
        print '====================================== experiment3'
        experiment3(first_video, last_video)
    elif config.options.experiment == 'create_video_captions':
        print '====================================== creating video captions'
        create_video_captions(first_video, last_video)
    elif config.options.experiment == 'compute_similarities':
        print '====================================== computing similarities'
        compute_similarities(first_video, last_video)
    else:
        print 'bye!'


# example call: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
