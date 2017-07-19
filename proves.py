import pickle


def main():
    tokens_set_to_load = "pickle/tokens_set.pickle"
    tokens_set = pickle.load(open(tokens_set_to_load, "rb"))
    import ipdb; ipdb.set_trace()
    # pickle.dump(config.tokens_set, open(config.tokens_set_to_load, "wb"))


if __name__ == "__main__":
    main()
