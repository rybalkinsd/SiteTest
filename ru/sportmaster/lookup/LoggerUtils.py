#logger init
import logging
import sys


def getLogger(out_stream=sys.stdout):
    logger = logging.getLogger('LoggerUtils.logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('/info.log')
    # handler = logging.StreamHandler(out_stream)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
