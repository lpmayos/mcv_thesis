import json
import time
import config
import numpy as np
import scipy
from commons import load_video_captions, plot_embeddings_with_labels
from data_structures.video_captions import VideoCaptions
import pickle


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
        print '\nvideo ' + str(video_id)
        video_captions = load_video_captions(video_id)

        # order_sentences_by_distance_to_mean(video_captions, True)
        embeddings = []
        labels = []
        for sentence in video_captions.sentences:
            embeddings.append(sentence.get_sentence_embedding(bfs))
            labels.append(sentence.sentence)

        embeddings_mean = np.mean(embeddings, axis=0)
        distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
        sort_index = np.argsort(distances)
        print 'Sentences from closest to fartest to the mean'
        for index in sort_index:
            print str(distances[index]) + ' \t ' + video_captions.get_sentence_text(index)

        if plot_embeddings:
            plot_embeddings_with_labels(embeddings, labels, 'sentence_embeddings_' + video_captions.video_id + '.png')


def experiment2(video_id_init, video_id_end):
    """ Goal: align concepts within captions of the same video.

    Method: TODO

    Results: TODO
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


if __name__ == '__main__':

    # create_video_captions(3000, 3010, 'closest')

    print '====================================== experiment1'
    experiment1(3000, 3010)
    # print '====================================== experiment2'
    # experiment2(3000, 3010)

    # create_video_captions(0, 3000)
    # create_video_captions(3000, 4500)  # done
    # create_video_captions(4500, 7010)
