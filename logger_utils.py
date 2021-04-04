import logging

LOG_LOCATION = '/var/log/urlstatus/error.log'

def bootstrap_logger(name, logfile=LOG_LOCATION):
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s (%(funcName)s, %(lineno)d) [%(levelname)s] - %(message)s")
    handler = logging.FileHandler(f'{logfile}')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
