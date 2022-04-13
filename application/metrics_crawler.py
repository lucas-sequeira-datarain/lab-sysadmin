from src.utils import update_metrics
from time import sleep

# Constants
SLEEP_TIME = 5 # seconds

# Main
if __name__ == "__main__":
    while True:
        try:
            update_metrics()
        except Exception as e:
            print(e)
        sleep(SLEEP_TIME)