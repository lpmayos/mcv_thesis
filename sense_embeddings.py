import json
import solr  # solrpy
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def plot_with_labels(low_dim_embs, labels, filename='tsne.png'):
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


def get_relevant_senses(word):
    # Returns set of relevant senses as decsribed in section 3.1 of SensEmbed:
    # Leaning Sense Embeddings for Word and Relational Similarity

    s = solr.SolrConnection('http://localhost:8983/solr/sensembed_vectors')
    word_senses1 = s.query('sense:' + word)
    word_senses2 = s.query('sense:' + word + '_bn*')
    return word_senses1.results + word_senses2.results


def main():

    wnl = WordNetLemmatizer()

    with open('/home/lpmayos/code/caption-guided-saliency/DATA/MSR-VTT/train_val_videodatainfo.json') as data_file:
        data = json.load(data_file)
        # data.get('info')             --> {u'contributor': u'Microsoft MSM group', u'version': u'1.0', u'year': u'2016', u'data_created': u'2016-04-14 14:30:20', u'description': u'This is 1.0 version of the 2016 MSR-VTT dataset.'}
        # len(data.get('videos'))       --> 7010
        # len(data.get('sentences'))    --> 140200

        video_id = 'video2962'
        # a man comparing two different people side by side
        # a man is explaining about something
        # a man is smoking a cigar
        # a man is talking about another man
        # a man is talking about something
        # a man points to a position on a map
        # a man talking while showing pictures of several men
        # a man talks about a series of men on screen
        # a person explaining about a place
        # a short foreign clip talking about two european men that are most likely famous
        # a slideshow of images play while a man narrates
        # different pictures are being shown of two different men
        # guy speaking in foreign language
        # person talking about actor
        # professional and ordinary photos are displaying
        # the photos flash by
        # there are some actors photos
        # a slideshow of images play while a man narrates
        # a man comparing two different people side by side
        # guy speaking in foreign language

        sentences_video = [a['caption'] for a in data['sentences'] if a['video_id'] == video_id]
        final_embeddings = []
        labels = []
        max_group_length = 5

        for sentence in sentences_video:
            text = word_tokenize(sentence)
            pos_tagged_text = nltk.pos_tag(text)

            for word_tag in pos_tagged_text:
                if word_tag[1] in ['NN', 'JJ', 'VB']:
                    word_senses = get_relevant_senses(word_tag[0].lower())
                    word_senses += get_relevant_senses(wnl.lemmatize(word_tag[0]))
                    for sense in word_senses:
                        if sense['sensembed'] not in final_embeddings:
                            final_embeddings.append(sense['sensembed'])
                            labels.append(sense['sense'])

            groups = []
            for group_length in range(2, max_group_length + 1):
                i = 0
                while i + group_length <= len(text):
                    group_text = text[i:i + group_length]
                    groups.append('_'.join([a.lower() for a in group_text]))
                    groups.append('_'.join([wnl.lemmatize(a) for a in group_text]))
                    i += 1

            for group in list(set(groups)):
                word_senses = get_relevant_senses(group)
                for sense in word_senses:
                    if sense['sensembed'] not in final_embeddings:
                        final_embeddings.append(sense['sensembed'])
                        labels.append(sense['sense'])

        tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
        low_dim_embs = tsne.fit_transform(final_embeddings)
        plot_with_labels(low_dim_embs, labels)


if __name__ == '__main__':
    main()
