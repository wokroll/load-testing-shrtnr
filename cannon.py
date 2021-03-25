import requests
import typing
import time
import logging

from utils import up_micronaut, down_micronaut, clean_db


logger = logging.getLogger(__name__)

class AppManager:

    app = None

    def __enter__(self):
        clean_db()
        self.app = up_micronaut()
        logger.info("Up Micronaut app!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        down_micronaut(self.app)
        clean_db()
        logger.info("Success down Micronaut app!")


class Cannon:
    """Клас який в выдповідає за те щоб "бомбити" сервіс"""

    # Пропорції скільки яких викликів викликатиметься
    LOGIN_C = 0.1
    SIGNUP_C = 0.1
    SET_C = 0.8
    GET_C = 99

    def __init__(self, url):
        self._URL = url

    def __login(self):
        pass

    def __signup(self):
        pass

    def __set_shrtnr(self):
        pass

    def __get_shrtner(self):
        pass

    def start_shoot(self, qps, duration,
                    login=None,
                    sign_up=None,
                    get=None,
                    set=None
                    ):
        if any(map(lambda x: x is None, [login, sign_up, get, set])):
            login = self.LOGIN_C
            sign_up = self.SIGNUP_C
            get = self.GET_C
            set = self.SET_C

        with AppManager():
            time.sleep(duration)

