import logging
import os
from datetime import datetime

def setup_logger(name, log_directory="logs", level=logging.INFO):
    """Function to set up logger by name and level"""

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
