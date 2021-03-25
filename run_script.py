import time

from utils import (
    up_micronaut,
    down_micronaut,
    clean_db
)


if __name__ == '__main__':
    clean_db()
    app = up_micronaut()
    time.sleep(30)
    down_micronaut(app)
    clean_db()
