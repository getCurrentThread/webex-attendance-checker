import logging
import datetime
import os.path

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(handlers=[logging.FileHandler(filename= os.path.join("logs",datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')) + 'log.txt',
                                                 encoding='utf-8', mode='a+')],
                    format='[%(asctime)s] %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO)


def getLogger(name):
    return logging.getLogger(name)
