from __future__ import print_function  # Only needed for Python 2
from selenium import webdriver


def find_element(driver, element, order):
    """
    """
    i = 0
    while i < 100:
        try:
            element = driver.find_elements_by_xpath(element)[order]
            return element
        except:
            i += 1
    return None


def generate_bibtex_file(docs):
    """
    """
    driver = webdriver.Chrome('/home/lpmayos/code/chromedriver')

    urls = []

    base_url = 'http://scholar.google.com/'
    for doc in docs:
        urls.append(base_url + 'scholar?hl=en&q=' + '+'.join(doc.split(' ')))

    with open('ref.bib', 'w') as f:
        for i, url in enumerate(urls):
            try:
                driver.get(url)

                element = find_element(driver, "//a[@class='gs_nph']", 1)
                element.click()

                element = find_element(driver, "//a[@class='gs_citi']", 0)
                element.click()

                element = find_element(driver, "//pre", 0)
                # print element.text

                print(element.text, file=f)
            except:
                print('[ERROR] Problem with file ' + docs[i] + ' (' + url + ')')
    f.close()

    # Close the browser!
    driver.quit()


def main():
    docs = ['Multi-Sentence Compression: Finding Shortest Paths in Word Graphs',
            'Abstractive Multi-Document Summarization via Phrase Selection and Merging *',
            'Deep Fusion LSTMs for Text Semantic Matching',
            'Multi-Structured Models for Transforming and Aligning Text',
            'From senses to texts: An all-in-one graph-based approach for measuring semantic similarity',
            'Distributional Measures of Semantic Distance: A Survey',
            'Knowledge Base Unification via Sense Embeddings and Disambiguation',
            'Supervised Sentence Fusion with Single-Stage Inference',
            'Multi-Sentence Compression: Finding Shortest Paths in Word Graphs',
            'Sentence Fusion via Dependency Graph Compression',
            'Sentence Fusion for Multidocument News Summarization',
            'Meteor Universal: Language Specific Translation Evaluation for Any Target Language',
            'CIDEr: Consensus-based Image Description Evaluation',
            'ROUGE: A Package for Automatic Evaluation of Summaries',
            'BLEU: a Method for Automatic Evaluation of Machine Translation',
            'Microsoft COCO Captions: Data Collection and Evaluation Server',
            'Describing Videos by Exploiting Temporal Structure',
            'SENSEMBED: Learning Sense Embeddings for Word and Relational Similarity',
            'Top-down Visual Saliency Guided by Captions',
            'Unsupervised Sentence Enhancement for Automatic Summarization',
            'SENSEMBED: Learning Sense Embeddings for Word and Relational Similarity',
            'Generating Video Description using Sequence-to-sequence Model with Temporal Attention',
            'Describing Videos using Multi-modal Fusion',
            'MSR-VTT: A Large Video Description Dataset for Bridging Video and Language Supplementary Material',
            'Show, Attend and Tell: Neural Image Caption Generation with Visual Attentio',
            'Boosting Video Description Generation by Explicitly Translating from Frame-Level Captions',
            'Semantic Compositional Networks for Visual Captioning',
            'Word2VisualVec: Image and Video to Sentence Matching by Visual Feature Predictio',
            'Video Summarization using Deep Semantic Features',
            'Deep Learning for Video Classification and Captioning',
            'Learning Language-Visual Embedding for Movie Understanding with Natural-Language',
            'Describing Videos using Multi-modal Fusion',
            'Adaptive Feature Abstraction for Translating Video to Language',
            'Video Captioning with Multi-Faceted Attention',
            'Multimodal Memory Modelling for Video Captioning',
            'Learning Spatiotemporal Features with 3D Convolutional Networks',
            'Multimodal Video Description',
            'Video Paragraph Captioning Using Hierarchical Recurrent Neural Networks',
            'Early Embedding and Late Reranking for Video Captioning',
            'Frame-and Segment-Level Features and Candidate Pool Evaluation for Video Caption Generation',
            'Natural language description of human activities from video images based on concept hierarchy of actions',
            'Corpus-Guided Sentence Generation of Natural Images',
            'Generating Natural-Language Video Descriptions Using Text-Mined Knowledge',
            'Improving LSTM-based Video Description with Linguistic Knowledge Mined from Text',
            'Integrating Language and Vision to Generate Natural Language Descriptions of Videos in the Wild',
            'Describing videos by exploiting temporal structure',
            'Deep Compositional Captioning: Describing Novel Object Categories without Paired Training Data',
            'Msr-vtt: A large video description dataset for bridging video and language',
            'Grounding Action Descriptions in Videos',
            'Translating video content to natural language descriptions',
            'Translating Videos to Natural Language Using Deep Recurrent Neural Networks',
            'Every picture tells a story: Generating sentences from images',
            'From captions to visual concepts and back',
            'Youtube2text: Recognizing and describing arbitrary activities using semantic hierarchies and zero-shot recognition',
            'A thousand frames in just a few words: Lingual description of videos through latent topics and sparse object stitching']
    generate_bibtex_file(docs)


if __name__ == "__main__":
    main()
