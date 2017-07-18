from nltk.translate.bleu_score import SmoothingFunction
# from nltk.translate.bleu_score import corpus_bleu

from nltk import bleu_score
# import nltk


def main():
    # hypothesis1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
    #                'ensures', 'that', 'the', 'military', 'always',
    #                'obeys', 'the', 'commands', 'of', 'the', 'party']
    # hypothesis2 = ['It', 'is', 'to', 'insure', 'the', 'troops',
    #                'forever', 'hearing', 'the', 'activity', 'guidebook',
    #                'that', 'party', 'direct']
    # reference1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
    #               'ensures', 'that', 'the', 'military', 'will', 'forever',
    #               'heed', 'Party', 'commands']
    # reference2 = ['It', 'is', 'the', 'guiding', 'principle', 'which',
    #               'guarantees', 'the', 'military', 'forces', 'always',
    #               'being', 'under', 'the', 'command', 'of', 'the',
    #               'Party']
    # reference3 = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
    #               'army', 'always', 'to', 'heed', 'the', 'directions',
    #               'of', 'the', 'party']

    # # From #1545 (https://github.com/nltk/nltk/pull/1545), BLEU is buggy for ngrams where the n<4.
    # # Solution: use SmoothingFunction (https://github.com/nltk/nltk/issues/1554)
    # chencherry = SmoothingFunction()
    # print bleu_score.sentence_bleu([reference1, reference2, reference3], hypothesis1, smoothing_function=chencherry.method4)
    # print bleu_score.sentence_bleu([reference1, reference2, reference3], hypothesis2, smoothing_function=chencherry.method4)

    sentences = ['a man is driving',
                 'a man is driving',
                 'a man driving a car',
                 'a man is driving a car',
                 'the man drives the car',
                 'a man is driving down a road',
                 'man talking about a car while driving',
                 'guy driving a car down the road',
                 'guy driving a car down the road',
                 'a man drives down the road in an audi',
                 'a man drives a vehicle through the countryside',
                 'the man driving the audi as smooth as possible',
                 'a person telling about a car',
                 'a man is driving in a car as part of a commercial',
                 'a person is driving his car around curves in the road',
                 'a man riding the car speedly in a narrow road',
                 'a man showing the various features of a car',
                 'a man silently narrates his experience driving an audi',
                 'a car is shown',
                 'a group is dancing']
    chencherry = SmoothingFunction()
    # for i, sentence1 in enumerate(sentences):
    #     sentence_scores = []
    #     for j, sentence2 in enumerate(sentences):
    #         if i != j:
    #             sentence_scores.append(bleu_score.sentence_bleu([a.split(' ') for j, a in enumerate(sentences) if i != j], sentence.split(' '), smoothing_function=chencherry.method4)
    sentences_scores = []
    for i, sentence1 in enumerate(sentences):
        scores = [bleu_score.sentence_bleu([sentence2.split(' ')], sentence1.split(' '), smoothing_function=chencherry.method4) for j, sentence2 in enumerate(sentences) if i != j]
        sentences_scores.append((sentence1, sum(scores) / len(scores)))
    sentences_scores.sort(key=lambda tup: tup[1], reverse=True)
    for sentence in sentences_scores:
        print sentence[0] + '(' + str(sentence[1]) + ')'


if __name__ == "__main__":
    main()
