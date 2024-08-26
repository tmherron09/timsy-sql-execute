import timsy_log
from timsy_log import get_logger_initialized
from timsy_config import Config

logger = timsy_log.getLogger('main')

if __name__ == '__main__':
    logger.info(get_logger_initialized())
    c = Config()
    logger.info(c.get('DEFAULT', 'loggerName'))
    pass
