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
parser.add_option('-x', '--solr_sensembed_path', help='Show info on command line')
parser.add_option('-y', '--path_to_train_val_videodatainfo', help='Path to train_val_videodatainfo.json')
parser.add_option('-z', '--path_to_new_train_val_videodatainfo', help='Path to new train_val_videodatainfo.json')
(options, args) = parser.parse_args()

if not options.experiment or not options.first or not options.last or not options.pickle_folder or not options.verbose or not options.solr_sensembed_path or not options.path_to_train_val_videodatainfo:
    print '[ERROR] Missing parameters. See config.py.'
    sys.exit(2)


first_video = int(options.first)
last_video = int(options.last)
experiment = options.experiment
folder = 'results_pmi_experiments/' + experiment
log_path = folder + '/' + experiment + '.log'


# Folder to save/load the pickle objects to/from
pickle_folder = options.pickle_folder


# Connection to solr server containing the sensembed vectors
solr_path = options.solr_sensembed_path
solr_connection = solr.SolrConnection(solr_path)


# Path to train_val_videodatainfo.json of MSR-VTT of caption-guided-saliency project
path_to_train_val_videodatainfo = options.path_to_train_val_videodatainfo
path_to_new_train_val_videodatainfo = options.path_to_new_train_val_videodatainfo


# If verbose, extra information is shown on shell
verbose = False
if options.verbose == 'true':
    verbose = True


# If an experiment is about to be launched, load token_set to use
# NOTE token_set is heavy, and takes some time to load.
if options.experiment:
    tokens_set_to_load = options.pickle_folder + "/tokens_set.pickle"

    try:
        tokens_set = pickle.load(open(tokens_set_to_load, "rb"))
    except (OSError, IOError):
        tokens_set = TokensSet()
