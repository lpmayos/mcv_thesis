import logging


def setup_logger(logger_name, log_file, level=logging.INFO):
    log = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    log.setLevel(level)
    log.addHandler(fileHandler)
    # log.addHandler(streamHandler)


def log_something(num):
    """
    """

    # configure logging file
    setup_logger(str(num), str(num) + '.log')
    log = logging.getLogger(str(num))
    log.info(num)


def main():
    for num in [0.12, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04]:
        log_something(num)


if __name__ == "__main__":
    main()
