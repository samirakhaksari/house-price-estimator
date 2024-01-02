import logging
from logging.handlers import RotatingFileHandler
from crawler import crawl_2nabsh_from_list
from models import export_csv
from train_new_data import train_regression_model

log_filename = 'daily_update.log'
max_log_size = 5 * 1024 * 1024
log_handler = RotatingFileHandler(log_filename, maxBytes=max_log_size, backupCount=3)
log_handler.setLevel(logging.ERROR)

logger = logging.getLogger('')
logger.addHandler(log_handler)

log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
log_handler.setFormatter(formatter)


def full_update_training():
    try:
        crawl_2nabsh_from_list()
        export_csv()
        train_regression_model('houses.csv')
        logger.info('Full training update completed successfully.')
    except Exception as e:
        logger.exception(f'An error occurred during full training update: {str(e)}')


if __name__ == '__main__':
    full_update_training()
