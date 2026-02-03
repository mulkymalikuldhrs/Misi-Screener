import logging
import sys
import os

def setup_logger(name: str = 'misi_screener', level: int = logging.INFO):
    """Sets up a centralized logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if not logger.handlers:
        # Create console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add ch to logger
        logger.addHandler(ch)

        # Optional: Add file handler
        log_file = os.environ.get('LOG_FILE', 'misi_screener.log')
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# Create a default logger instance
logger = setup_logger()
