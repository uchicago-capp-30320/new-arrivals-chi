import logging
import os
from datetime import datetime

def setup_logger(name: str, log_directory: str="logs", level = logging.INFO) -> logging.Logger:
    """
    Set up and configure a logger.

    This function creates a logger with both file and console handlers.
    It also supports different logging levels.

    Parameters:
        name (str): "main", "database", etc.
        log_directory (str): Directory where the log files will be stored. Default is 'logs'.
        level (int): The logging level, which determines the severity of the events that are logged.
                     This can be DEBUG, INFO, WARNING, ERROR, or CRITICAL. Default is INFO.

    Logging Levels:
        DEBUG: Detailed information, typically useful only when diagnosing problems.
        INFO: Confirmation that things are working as expected.
        WARNING: An indication that something unexpected happened, or indicative of near-term problems.
        ERROR: A significant problem occurred, preventing some function from completing.
        CRITICAL: A serious error

    Returns:
        logging.Logger: A configured logger with specified name and level.

    Example:
        logger = setup_logger('main', level=logging.DEBUG)
        logger.debug('debug')
        logger.info('info')
        logger.warning('warning')
        logger.error('error')
        logger.critical('critical')
    """
    # Ensure that a logs directory exists
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Generate a timestamped log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"{name}_{timestamp}.log"
    log_path = os.path.join(log_directory, log_filename)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create file handler for logging to a file
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    # Create console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
