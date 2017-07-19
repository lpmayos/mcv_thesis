import sys
import os
import pickle
from data_structures.tokens_set import TokensSet
from optparse import OptionParser
import solr  # corresponds to solrpy


def config_ths_and_paths(th1, th2, experiment):
    """
    """
    if th1:
        th1 = float(th1)  # corresponds to minimum_token_similarity
        sufix_files = experiment[0] + experiment[-1] + '_th1_' + str(th1) + '_th2_' + str(th2)
        folder = 'results/' + experiment + '/th1_' + str(th1)
        boxplot_path = folder + '/boxplot_' + experiment[0] + experiment[-1] + '_th1_' + str(th1) + '.png'
        barchart_path = folder + '/barchart_' + experiment[0] + experiment[-1] + '_th1_' + str(th1) + '_th2_' + str(th2) + '.png'
        log_path = folder + '/' + experiment[0] + experiment[-1] + '_th1_' + str(th1) + '.log'
        if not os.path.exists(folder):
            os.makedirs(folder)
    else:
        th1 = None
        sufix_files = experiment[0] + experiment[-1] + '_th2_' + str(th2)
        folder = 'results/' + experiment
        boxplot_path = folder + '/' + 'boxplot_' + experiment[0] + experiment[-1] + '.png'
        barchart_path = folder + '/barchart_' + experiment[0] + experiment[-1] + '_th2_' + str(th2) + '.png'
        log_path = folder + '/' + experiment[0] + experiment[-1] + '.log'
        if not os.path.exists(folder):
            os.makedirs(folder)

    return experiment, th1, th2, sufix_files, folder, boxplot_path, barchart_path, log_path


# Parse command line args and make sure all params are present
parser = OptionParser()
parser.add_option('-p', '--pickle_folder', help='Path to folder containing the pickle files to use')
parser.add_option('-e', '--experiment', help='Experiment name (see main function in experiments.py for options)')
parser.add_option('-a', '--th1', help='corresponds to minimum_token_similarity')
parser.add_option('-s', '--first', help='First video number [0-7010]')
parser.add_option('-l', '--last', help='Last video number [0-7010]')
parser.add_option('-v', '--verbose', help='Show info on command line')
parser.add_option('-x', '--solr_sensembed_path', help='Show info on command line')
parser.add_option('-y', '--path_to_train_val_videodatainfo', help='Path to train_val_videodatainfo.json')
parser.add_option('-z', '--create_new_training_sentences', help='true if we want to generate new training sentences')
(options, args) = parser.parse_args()

if not options.experiment or not options.first or not options.last or not options.pickle_folder or not options.verbose or not options.solr_sensembed_path or not options.path_to_train_val_videodatainfo or not options.create_new_training_sentences:
    print '[ERROR] Missing parameters. See config.py.'
    sys.exit(2)


first_video = int(options.first)
last_video = int(options.last)


# Similarity strategy to use when comparing tokens, as described in  algorithm 1
# of senseEmbed paper. For now the only option is the 'closest' strategy.
# TODO lpmayos: add 'weighted' strategy
similarity_strategy = 'closest'


# Threshold to consider in experiments
#       th1 corresponds to minimum_token_similarity
experiment, th1, th2, sufix_files, folder, boxplot_path, barchart_path, log_path = config_ths_and_paths(options.th1, None, options.experiment)


# Folder to save/load the pickle objects to/from
pickle_folder = options.pickle_folder


# Connection to solr server containing the sensembed vectors
solr_path = options.solr_sensembed_path
solr_connection = solr.SolrConnection(solr_path)


# Path to train_val_videodatainfo.json of MSR-VTT of caption-guided-saliency project
path_to_train_val_videodatainfo = options.path_to_train_val_videodatainfo


# If verbose, extra information is shown on shell
verbose = False
if options.verbose == 'true':
    verbose = True


create_new_training_sentences = False
if options.create_new_training_sentences == 'true':
    create_new_training_sentences = True


# When launching experiments that would change the previously created pickle
# files, if they exist, warn the user:
if options.experiment == 'create_video_captions':
    print 'If they exist, this will change the existing pickle. Do you want to proceed? yes/no'
    choice = raw_input().lower()
    if choice != 'yes':
        print 'aborting mission ;)'
        options.experiment = None


# If an experiment is about to be launched, load token_set to use
# NOTE token_set is heavy, and takes some time to load.
if options.experiment:
    tokens_set_to_load = options.pickle_folder + "/tokens_set.pickle"

    try:
        tokens_set = pickle.load(open(tokens_set_to_load, "rb"))
    except (OSError, IOError):
        tokens_set = TokensSet()
