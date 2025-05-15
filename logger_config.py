import logging

# Create and configure logger named "chess"
logger = logging.getLogger("chess")
logger.setLevel(logging.INFO)

# Avoid adding duplicate handlers if this file is imported multiple times
if not logger.handlers:
    # Define log message format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler - saves logs to a file
    file_handler = logging.FileHandler("chess_log.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler - prints logs to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

