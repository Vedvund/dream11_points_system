from datetime import datetime
import logging
import os

from utils.helper.file_helper import get_root_dir


def setup_logging():
    # Create a logs directory if it doesn't exist
    log_dir = os.path.join(get_root_dir(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Construct the log file path using os.path.join
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(filename)s:L%(lineno)d - %(levelname)s\t-\t%(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging
