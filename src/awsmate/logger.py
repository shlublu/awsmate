import logging

defaultLevel = logging.INFO

logging.basicConfig(format = '%(message)s', level = defaultLevel)

logger = logging.getLogger()
logger.setLevel(defaultLevel)
