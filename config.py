import sys
import pickle
from data_structures.tokens_set import TokensSet
from optparse import OptionParser
import solr  # corresponds to solrpy


# Parse command line args and make sure all params are present
parser = OptionParser()
parser.add_option('-p', '--pickle_folder', help='Path to folder containing the pickle files to use')
parser.add_option('-e', '--experiment', help='Experiment name (see main function in experiments.py for options)')
parser.add_option('-s', '--first', help='First video number [0-7010]')
parser.add_option('-l', '--last', help='Last video number [0-7010]')
parser.add_option('-v', '--verbose', help='Show info on command line')
(options, args) = parser.parse_args()

if not options.experiment or not options.first or not options.last or not options.pickle_folder or not options.verbose:
    print '[ERROR] Usage: python experiments.py -p pickle -e experiment1 -s 3000 -l 3010 -v true'
    sys.exit(2)

# Similarity strategy to use when comparing tokens, as described in  algorithm 1
# of senseEmbed paper. For now the only option is the 'closest' strategy.
# TODO lpmayos: add 'weighted' strategy
similarity_strategy = 'closest'

# When launching experiments that would change the previously created pickle
# files, if they exist, warn the user:
if options.experiment == 'create_video_captions':
    print 'If they exist, this will change the existing pickle. Do you want to proceed? yes/no'
    choice = raw_input().lower()
    if choice != 'yes':
        print 'aborting mission ;)'
        options.experiment = None

# If verbose, extra information is shown on shell
if options.verbose == 'true':
    verbose = True
else:
    verbose = False

# If an experiment is about to be launched, load token_set to use, and create
# variables for pickle folder and the connection to solr.
# NOTE token_set is heavy, and takes some time to load.
if options.experiment:
    tokens_set_to_load = options.pickle_folder + "/tokens_set.pickle"

    try:
        tokens_set = pickle.load(open(tokens_set_to_load, "rb"))
    except (OSError, IOError):
        tokens_set = TokensSet()

    pickle_folder = options.pickle_folder

    solr_connection = solr.SolrConnection('http://localhost:8983/solr/sensembed_vectors')
