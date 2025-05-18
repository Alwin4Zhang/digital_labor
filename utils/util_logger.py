import os
import logging
import sys
sys.path.append("./")

LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"

# logging.basicConfig(format=LOG_FORMAT)
logging.basicConfig(
    filename="./app.log",  # Specify the log file name
    filemode="a",
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log message format
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)