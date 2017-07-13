import itertools
import numpy as np
import config
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pickle
import json
import logging


def setup_logger(logger_name, log_file, level=logging.INFO):
    log = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    log.setLevel(level)
    log.addHandler(fileHandler)
    # log.addHandler(streamHandler)


def get_relevant_senses(word):
    # Returns set of relevant senses as described in section 3.1 of SensEmbed:
    # Leaning Sense Embeddings for Word and Relational Similarity

    word_senses1 = config.solr_connection.query('sense:' + word + '_bn*')
    word_senses2 = config.solr_connection.query('sense:' + word)
    return word_senses1.results + word_senses2.results


def tanimoto_distance(w1, w2):
    """
    """
    return np.dot(w1, w2) / ((np.linalg.norm(w1, 2))**2 + (np.linalg.norm(w2, 2))**2 - np.dot(w1, w2))


def word_similarity_closest(token1, token2):
    """ implementation of the word similarity measure described in algorithm 1
    of senseEmbed paper using the 'closest' strategy
    """
    if (token1.id, token2.id) in config.tokens_set.tokens_similarities_closest:
        similarity = config.tokens_set.tokens_similarities_closest[(token1.id, token2.id)]
    elif token1.id == token2.id:
        similarity = 1.0
    else:
        senses_combinations = list(itertools.product(token1.senses, token2.senses))
        similarity = -1
        for sense_combination in senses_combinations:
            similarity = max(similarity, tanimoto_distance(sense_combination[0].sensembed, sense_combination[1].sensembed))
    return similarity


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


def load_video_captions(video_id):
    """
    """
    video_captions = pickle.load(open(config.pickle_folder + "/video_captions_" + str(video_id) + ".pickle", "rb"))
    return video_captions


def remove_training_sentences(sentences_to_remove):
    """ Load the video annotations from json file, and makes a copy removing the
    sentences indicated in sentences_to_remove, adding a sufix to the file name.
    """
    if config.pickle_folder == 'pickle' and config.first_video == 0 and config.last_video == 7010 and config.create_new_training_sentences:
        print 'generating new training sentences...'
        with open(config.path_to_train_val_videodatainfo) as data_file:
            data = json.load(data_file)
            data_positions_to_remove = []
            for sentence_to_remove in sentences_to_remove:
                data_position = [i for i, a in enumerate(data['sentences']) if a['caption'] == sentence_to_remove[0].sentence and a['video_id'] == 'video' + str(sentence_to_remove[1])]
                data_positions_to_remove.append(data_position[0])
        new_data_sentences = [a for i, a in enumerate(data['sentences']) if i not in data_positions_to_remove]

        data['sentences'] = new_data_sentences

        new_file_path = config.path_to_train_val_videodatainfo.split('.json')[0] + '_' + config.sufix_files + '.json'
        with open(new_file_path, 'w') as outfile:
            json.dump(data, outfile)
        print 'done generating new training sentences!'
    else:
        print '[WARNING] New json file for training not created'
    return


def generate_boxplot(all_videos_sentences_similarities, th1=None):
    """
    """

    # boxplot with outliers
    plt.figure()

    # get dictionary returned from boxplot
    bp_dict = plt.boxplot(all_videos_sentences_similarities, vert=False)

    for line in bp_dict['medians']:
        x, y = line.get_xydata()[1]  # position for median line: [1] top of median line, [0] bottom of median line
        plt.text(x, y + 0.02, '%.3f' % x, horizontalalignment='center')  # overlay median value above, centered

    for line in bp_dict['boxes']:
        x, y = line.get_xydata()[0]  # bottom of left line
        plt.text(x, y - 0.02, '%.3f' % x, horizontalalignment='center', verticalalignment='top')
        x, y = line.get_xydata()[3]  # bottom of right line
        plt.text(x, y - 0.02, '%.3f' % x, horizontalalignment='center', verticalalignment='top')

    for line in bp_dict['whiskers']:
        x, y = line.get_xydata()[1]
        plt.text(x, y - 0.08, '%.3f' % x, horizontalalignment='center')

    # plt.show()
    plt.savefig(config.boxplot_path)
    plt.close()


def generate_barchart(num_sentences_discarded):
    """
    """
    plt.jet()
    lines = plt.plot(range(config.first_video, config.last_video), num_sentences_discarded)
    plt.setp(lines, linewidth=2, color='r')
    plt.xlabel('Training videos')
    plt.ylabel('Discarded sentences')
    # plt.title('Discarded sentences per video')

    plt.grid(True)
    # plt.show()
    plt.savefig(config.barchart_path)
    plt.close()
