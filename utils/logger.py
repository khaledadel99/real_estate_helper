import time
import logging
from functools import wraps

# Configure logging once (you can customize this)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.info(f"Started '{func.__name__}'")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.warning(f"error with {func.__name__} : {e}")
        finally:
            elapsed = time.time() - start_time
            logging.info(f"Finished '{func.__name__} 'in {elapsed:.2f} seconds")
    return wrapper
