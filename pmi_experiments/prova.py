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


if __name__ == "__main__":
    # lemma pos
    # pmi sino existe 0, si no ocurren juntas -1, corpus british National Corpus
    candidates = ['car NN', 'vehicle NN', 'audi NN']
    context = ['drives', 'countryside', 'road', 'driving', 'commercial', 'speedly', 'narrow road', 'features', 'showing', 'narrates', 'experience', 'curves', 'telling', 'talking', 'smooth']
    context = ['drive VB*']

    for candidate in candidates:
        pmi = do_pmi([candidate], context)
        print pmi

    # for term in terms:
    #     if term.endswith(" NN"):
    #         terms.remove(term)
    #         print term, do_pmi([term], terms)
    #         print "truck", do_pmi(["truck NN"], terms)
    #         terms.add(term)
