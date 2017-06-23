import pickle
from data_structures.tokens_set import TokensSet

# tokens_set_to_load = "pickle/tokens_set.pickle"
tokens_set_to_load = "pickle/tokens_set_3000_3010.pickle"

try:
    tokens_set = pickle.load(open(tokens_set_to_load, "rb"))
except (OSError, IOError):
    tokens_set = TokensSet()
