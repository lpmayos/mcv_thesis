import sys
import pickle
from data_structures.tokens_set import TokensSet
from optparse import OptionParser
import solr  # corresponds to solrpy


parser = OptionParser()
parser.add_option('-p', '--pickle_folder', help='path to folder containing the pickles to use')
parser.add_option('-e', '--experiment', help='write experiment name')
parser.add_option('-s', '--first', help='write first video number')
parser.add_option('-l', '--last', help='write last video number')
parser.add_option('-v', '--verbose', help='show info on command line')
(options, args) = parser.parse_args()

if not options.experiment or not options.first or not options.last or not options.pickle_folder or not options.verbose:
    print '[ERROR] Usage: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010 -v false'
    sys.exit(2)

similarity_strategy = 'closest'

# check if the experiment to launch is about to create/modify the pickles, and warn the user:
if options.experiment == 'create_video_captions':
    print 'If they exist, this will change the existing pickle. Do you want to proceed? yes/no'
    choice = raw_input().lower()
    if choice != 'yes':
        print 'aborting mission ;)'
        options.experiment = None

if options.verbose == 'true':
    verbose = True
else:
    verbose = False

if options.experiment:
    tokens_set_to_load = options.pickle_folder + "/tokens_set.pickle"

    try:
        tokens_set = pickle.load(open(tokens_set_to_load, "rb"))
    except (OSError, IOError):
        tokens_set = TokensSet()

    pickle_folder = options.pickle_folder

    solr_connection = solr.SolrConnection('http://localhost:8983/solr/sensembed_vectors')
