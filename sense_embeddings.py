import json
import pprint
import scipy
import numpy as np
from annotation import Annotation
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def compute_distance_matrix(vectors):
    distance_matrix = np.empty((len(vectors), len(vectors)))
    i = 0
    j = 0
    for vector1 in vectors:
        for vector2 in vectors:
            if i == j:
                distance = float('inf')
            else:
                distance = scipy.spatial.distance.cosine(vector1, vector2)
            distance_matrix[i][j] = distance
            j += 1
        i += 1
        j = 0
    return distance_matrix


def compute_distances_sense(senses):
    distance_matrix = np.empty((len(senses), len(senses)))
    i = 0
    j = 0
    for sense1 in senses:
        for sense2 in senses:
            if sense1['id'].split('_')[0] == sense2['id'].split('_')[0]:
                distance = float('inf')
            else:
                distance = scipy.spatial.distance.cosine(sense1['sensembed'], sense2['sensembed'])
            distance_matrix[i][j] = distance
            j += 1
        i += 1
        j = 0
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(distance_matrix)


def _plot_embeddings_with_labels(embeddings, labels, filename='tsne.png'):

    # dimensionality reduction with PCA
    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
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


def order_sentences_by_distance_to_mean(annotation):
    """ orders the sentences of the annotation by distance to the mean;
    the mean is computed as the sum of the sensembeds of all possible sense of all the tokens of a sentence.
    """
    embeddings = []
    labels = []
    for sentence in annotation.sentences:
        embeddings.append(annotation.get_sentence_embedding(sentence['sentence_id'] - 1))
        labels.append(sentence['sentence'])

    embeddings_mean = np.mean(embeddings, axis=0)
    distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
    sort_index = np.argsort(distances)
    print 'Sentences from closest to fartest to the mean'
    for index in sort_index:
        print str(distances[index]) + ' \t ' + annotation.get_sentence_text(index)


def order_sentences_by_distance_to_mean_BFS(annotation):
    """ orders the sentences of the annotation by distance to the mean;
    the mean is computed as the sum of the sensembeds of all possible sense of all the tokens of a sentence.
    """
    embeddings = []
    labels = []
    for sentence in annotation.sentences:
        embeddings.append(annotation.get_sentence_embedding_BFS(sentence['sentence_id'] - 1))
        labels.append(sentence['sentence'])

    embeddings_mean = np.mean(embeddings, axis=0)
    distances = [scipy.spatial.distance.cosine(embedding, embeddings_mean) for embedding in embeddings]
    sort_index = np.argsort(distances)
    for index in sort_index:
        print str(distances[index]) + ' \t ' + annotation.get_sentence_text(index)


def main():

    with open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json') as data_file:
        data = json.load(data_file)
        # data.get('info')             --> {u'contributor': u'Microsoft MSM group', u'version': u'1.0', u'year': u'2016', u'data_created': u'2016-04-14 14:30:20', u'description': u'This is 1.0 version of the 2016 MSR-VTT dataset.'}
        # len(data.get('videos'))       --> 7010
        # len(data.get('sentences'))    --> 140200

        # --> I want to disciver that "two european men" corresponds to "two different people" and to "some actors"
        # for each sense of each word of each sentence, compare to all senses of all words of all other senses and save minimum distance
        #       --> ie. man - man 0; man - explaining 100; man something 90
        #       --> relate words or groups of words closest for each pair of sentences

        # once we have stored the info of all possible senses of all tokens of
        # all sentences, we need to find for each token of each sentence which
        # of the tokens of every other sentence is closer.
        #       --> concept alignment if distance below threshold

        # compute_distances(annotation.senses)

        for video_id in range(2949, 2990):
            print '\nvideo ' + str(video_id)
            annotation = Annotation(data, 'video' + str(video_id))
            order_sentences_by_distance_to_mean_BFS(annotation)

        # distance_matrix = compute_distance_matrix(embeddings)
        # sum_of_distances = [sum(filter(lambda x: x != float('inf'), a)) for a in distance_matrix]

        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(distance_matrix)

        # annotation._plot_embeddings_with_labels(embeddings, labels, 'embedded_sentences' + video_id + '.png')


if __name__ == '__main__':
    main()
