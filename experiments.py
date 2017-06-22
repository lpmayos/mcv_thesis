import json
import scipy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from video_captions import VideoCaptions
import pickle
import time
import config


def plot_embeddings_with_labels(embeddings, labels, filename='tsne.png'):

    # dimensionality reduction with PCA
    tsne = TSNE(perplexity=50, n_components=2, init='pca', n_iter=5000)
    low_dim_embs = tsne.fit_transform(embeddings)

    assert low_dim_embs.shape[0] >= len(labels), "More labels than embeddings"
    plt.figure(figsize=(18, 18))  # in inches
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        plt.scatter(x, y)
        plt.annotate(label,
                     xy=(x, y),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')

    plt.savefig(filename)


def order_sentences_by_distance_to_mean(video_captions, bfs, plot_embeddings=False):
    """ orders the sentences of the video_captions by distance to the mean;
    if bfs, the mean is computed as the sum of the sensembeds of **the first** sense of all the tokens of a sentence.
    else, the mean is computed as the sum of the sensembeds of **all possible** senses of all the tokens of a sentence.
    """
    embeddings = []
    labels = []
    for sentence in video_captions.sentences:
        embeddings.append(sentence.get_sentence_embedding(bfs))
        labels.append(sentence.get_sentence())

    embeddings_mean = np.mean(embeddings, axis=0)
    distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
    sort_index = np.argsort(distances)
    print 'Sentences from closest to fartest to the mean'
    for index in sort_index:
        print str(distances[index]) + ' \t ' + video_captions.get_sentence_text(index)

    if plot_embeddings:
        plot_embeddings_with_labels(embeddings, labels, 'sentence_embeddings_' + video_captions.video_id + '.png')


def experiment1(video_id1, video_id2):
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
    with open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json') as data_file:
        data = json.load(data_file)
        # data.get('info')             --> {u'contributor': u'Microsoft MSM group', u'version': u'1.0', u'year': u'2016', u'data_created': u'2016-04-14 14:30:20', u'description': u'This is 1.0 version of the 2016 MSR-VTT dataset.'}
        # len(data.get('videos'))       --> 7010
        # len(data.get('sentences'))    --> 140200

        for video_id in range(video_id1, video_id2):
            print '\nvideo ' + str(video_id)
            video_captions = VideoCaptions(data, 'video' + str(video_id))
            order_sentences_by_distance_to_mean(video_captions, True)


def experiment2(video_id1, video_id2):
    """ Goal: align concepts within captions of the same video.

    Method: TODO

    Results: TODO
    """

    with open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json') as data_file:

        data = json.load(data_file)  # TODO lpmayos: probably not a good idea to load it for every non-existing video ;)

        for video_id in range(video_id1, video_id2):
            start = time.time()
            print '\n\n***** video ' + str(video_id)
            try:
                video_captions = pickle.load(open("pickle/video_captions_" + str(video_id) + ".pickle", "rb"))
            except (OSError, IOError):
                video_captions = VideoCaptions(data, 'video' + str(video_id))
                video_captions.compute_all_tokens_similarity()
                pickle.dump(video_captions, open("pickle/video_captions_" + str(video_id) + ".pickle", "wb"))
            end = time.time()
            print str(end - start) + ' seconds'

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

    pickle.dump(config.tokens_set, open("pickle/tokens_set.pickle", "wb"))


if __name__ == '__main__':

    experiment2(2935, 2947)
