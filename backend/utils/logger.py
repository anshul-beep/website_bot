import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True) 

log_file = os.path.join(log_dir, "app.log")

# Create logging config
logging.basicConfig(
    filename=log_file,
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def get_logger(name):
    return logging.getLogger(name)