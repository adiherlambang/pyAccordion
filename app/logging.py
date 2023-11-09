import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

current_date = datetime.now().strftime('%Y-%m-%d')


def configure_logger(app):
    # Define log file path
    log_file = 'app/logs/application.log'

    # Check if the log file exists, and create it if it doesn't
    if not os.path.isfile(log_file):
        open(log_file, 'w').close()

    # Set the log level
    log_level = logging.INFO

    # Create a formatter for log messages
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')

    # Create a file handler that logs to a file
    file_handler = RotatingFileHandler(log_file, maxBytes=50000000, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    # Add the file handler to the app's logger
    app.logger.addHandler(file_handler)

    # Set the app's log level
    app.logger.setLevel(log_level)