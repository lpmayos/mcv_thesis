import sys
import getopt
import json
import time
import config
import numpy as np
import scipy
from commons import load_video_captions, plot_embeddings_with_labels
from data_structures.video_captions import VideoCaptions
import pickle


def create_video_captions(video_id_init, video_id_end, compute_similarity=False):
    """ NOTE: it does NOT check if the pickle object exist, it creates it and overwrittes the old one if it exists
    """
    with open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json') as data_file:

        data = json.load(data_file)
        for video_id in range(video_id_init, video_id_end):
            video_captions = VideoCaptions(data, 'video' + str(video_id))
            if compute_similarity == 'closest':
                video_captions.compute_all_tokens_similarity()
            pickle.dump(video_captions, open("pickle/video_captions_" + str(video_id) + ".pickle", "wb"))
            pickle.dump(config.tokens_set, open(config.tokens_set_to_load, "wb"))  # no me conviene hacerlo cada vez si estoy haciendo el dump de muchos videos


def experiment1(video_id_init, video_id_end):
    """ Goal: detect those captions that are wrong: they have typos or are
    not descriptive.

    Method: for each video we get all the captions and we compute an
    embedding for all the sentences. Then, we project all the embeddings
    in common space, we compute its centroid and the distances to the
    centroid of each embedding, sorting the captions by distance.
    Then, we can discard the highest percentage (i.e. 10%) or the ones that
    are above a certain threshold.

    Results: a sample of the results (sentence ordering and image of the
    embedding space) can be seen at results/experiment1/
    """
    bfs = True
    plot_embeddings = False

    for video_id in range(video_id_init, video_id_end):
        video_captions = load_video_captions(video_id)

        embeddings = []
        labels = []
        for sentence in video_captions.sentences:
            embeddings.append(sentence.get_sentence_embedding(bfs))
            labels.append(sentence.sentence)

        embeddings_mean = np.mean(embeddings, axis=0)
        distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
        sort_index = np.argsort(distances)
        print '\n\n ***** video ' + str(video_id) + '. Sentences from closest to fartest to the mean:\n'
        for index in sort_index:
            print str(distances[index]) + ' \t ' + video_captions.get_sentence_text(index)

        if plot_embeddings:
            plot_embeddings_with_labels(embeddings, labels, 'sentence_embeddings_' + video_captions.video_id + '.png')


def experiment2(video_id_init, video_id_end):
    """ Goal: for each token of each sentence, computes which of the tokens of
    every other sentence is closer and shows it on shell.

    Method: in config.tokens_set we have computed the similarity of every pair
    of tokens, so we just loop over all of them and keep the most similar.

    Results:  a sample of the results can be seen at results/experiment2/most_similar_tokens.txt
    """
    for video_id in range(video_id_init, video_id_end):
        video_captions = load_video_captions(video_id)

        start = time.time()
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

        end = time.time()
        print str(end - start) + ' seconds'


def experiment3(video_id_init, video_id_end):
    """ Goal: compute sentences similarity and rank them.

    Method: for each pair of sentences, compute their similarity (non-symmetric)
    as the sum of the distances of each token in one sentence to the closest one
    in the other sentence, dividing by the number of tokens added.

    Results:
    """
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
        print '\n\n ***** video ' + str(video_id) + '. Sentences from most similar to all others to most different to all others:\n'
        for sentence_index in sentences_order:
            print '\t' + video_captions.sentences[sentence_index].sentence + ' (' + str(sentences_global_similarities[sentence_index]) + ')'


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
        create_video_captions(first_video, last_video)  # TODO lpmayos 3000 - 4500 already done


# example call: python experiments.py -t tokens_set.pickle -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
