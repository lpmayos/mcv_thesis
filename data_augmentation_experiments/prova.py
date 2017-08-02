#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2
import urllib

import conll

EN_PARSER = "http://services-taln.s.upf.edu:8080/prod/transition-service/en/parse"
ES_PARSER = "http://multisensor-taln.s.upf.edu:8080/prod/transition-service/es/parse"


class TransitionClient(object):

    def __init__(self, parser_url):
        self.parser_url = parser_url

    def parse_text(self, text):

        params = u"text=%s" % (urllib.quote(text))
        request = urllib2.urlopen(self.parser_url, params)

        response = json.loads(request.read())

        if "error" in response:
            raise Exception(response["error"])

        return conll.ConllStruct(response["output"].encode('utf8'))


def do_pmi(combination_words, context_words):

    solr_url = "http://10.80.27.67:8080/solr/bnc/"

    param_dict = {"solr_url": solr_url,
                  "combination_words": combination_words,
                  "context_words": context_words}

    params = urllib.urlencode(param_dict, True)
    request = urllib2.urlopen("http://10.80.27.67/webservice/test_context_pmi?" + params)

    response = json.loads(request.read())

    if "error" in response:
        raise Exception(response["error"])

    return response


# def extract_parts(output):
#     """
#     """
#     import ipdb; ipdb.set_trace()
#     sbj = [a for a in sentence if a.deprel == 'SBJ'][0]
#     # buscar quien le referencia, y quien referencia a ese, etc. hasta llegar a id '0'

#     # while aux != for sentence in output:
#     #     for token in sentence:
#     #         import ipdb; ipdb.set_trace()
#     #         print token
#     #         # terms.add(token.lemma + " " + token.pos)


if __name__ == "__main__":

    text = "My horse's car is red."
    text = "Two men discuss education and philanthropy on a news program"

    parser_en = TransitionClient(EN_PARSER)
    output = parser_en.parse_text(text)
    print '\n%s\n', output

    for sentence in output:
        subject, predicate = sentence.get_subject_and_predicate()
        import ipdb; ipdb.set_trace()
        print 'babau'

    # for term in terms:
    #     if term.endswith(" NN"):
    #         terms.remove(term)
    #         print term, do_pmi([term], terms)
    #         print "truck", do_pmi(["truck NN"], terms)
    #         terms.add(term)

    # print '\n\n\n'
