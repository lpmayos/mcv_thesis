import pickle
from data_structures.tokens_set import TokensSet

try:
    tokens_set = pickle.load(open("pickle/tokens_set.pickle", "rb"))
except (OSError, IOError):
    tokens_set = TokensSet()
