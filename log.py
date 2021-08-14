import logging

LOG_LEVEL = logging.INFO


class Log:

    def __init__(self):
        logger = logging.getLogger(__name__)
        fl = logging.FileHandler(filename='./log/pi-camera.log')
        logger.addHandler(fl)
        logger.setLevel(LOG_LEVEL)
        fl.setLevel(LOG_LEVEL)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%dT%H:%M:%S")
        fl.setFormatter(fmt)
        self.logger = logger

    def log_info(self, msg):
        self.logger.info(msg=msg)

    def log_warn(self, msg):
        self.logger.warning(msg=msg)

    def log_error(self, msg):
        self.logger.error(msg=msg)
