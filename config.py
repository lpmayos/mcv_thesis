import sys
import pickle
from data_structures.tokens_set import TokensSet
from optparse import OptionParser

# example call: python experiments.py -t tokens_set.pickle -e experiment1 -s 3000 -l 3010
parser = OptionParser()
parser.add_option('-t', '--tokens_set', help='write tokens_set to use (tokens_set.pickle, tokens_set_3000_3010.pickle)')
parser.add_option('-e', '--experiment', help='write experiment name')
parser.add_option('-s', '--first', help='write first video number')
parser.add_option('-l', '--last', help='write last video number')
(options, args) = parser.parse_args()

if not options.experiment or not options.first or not options.last or not options.tokens_set:
    print '[ERROR] Usage: python experiments.py -t tokens_set.pickle -e experiment1 -s 3000 -l 3010'
    sys.exit(2)


# tokens_set_to_load = "pickle/tokens_set.pickle"
tokens_set_to_load = 'pickle/' + options.tokens_set

try:
    tokens_set = pickle.load(open(tokens_set_to_load, "rb"))
except (OSError, IOError):
    tokens_set = TokensSet()
