#logger init
import logging
import sys


def getLogger(out_stream='info.out'):
    logger = logging.getLogger('LoggerUtils.logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('info.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
