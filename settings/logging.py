import logging


def get_logger(name, level):
    logger = logging.getLogger(name=name)

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    if level >= 4:
        stream_handler.setLevel(logging.DEBUG)
    elif level == 3:
        stream_handler.setLevel(logging.INFO)
    elif level == 2:
        stream_handler.setLevel(logging.WARNING)
    elif level == 1:
        stream_handler.setLevel(logging.ERROR)
    else:
        stream_handler.setLevel(logging.CRITICAL)

    logger.addHandler(stream_handler)
    return logger