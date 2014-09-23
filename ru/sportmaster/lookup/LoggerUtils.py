#logger init
import logging
import sys


def getFileLogger(out_filename='info.out'):
    logger = logging.getLogger('file_logger' + out_filename)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(out_filename)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def getStreamLogger(out_stream=sys.stdout):
    logger = logging.getLogger('Stream logger')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(out_stream)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

