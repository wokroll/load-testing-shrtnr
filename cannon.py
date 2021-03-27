import requests
import time
import random
import logging
import json
import string
from typing import List
from concurrent.futures import ThreadPoolExecutor, wait

from utils import up_micronaut, down_micronaut, clean_db


logger = logging.getLogger(__name__)
HEADERS = {"Content-Type": "application/json"}


class AppManager:

    app = None

    def __init__(self, url):
        self.url = url

    def __enter__(self):
        clean_db()
        self.app = up_micronaut()
        logger.info("Up Micronaut app!")
        time.sleep(3)

    def __exit__(self, exc_type, exc_val, exc_tb):
        down_micronaut(self.app)
        clean_db()
        logger.info("Success down Micronaut app!")


class Cannon:
    """Клас який в выдповідає за те щоб "бомбити" сервіс"""

    # Пропорції скільки яких викликів викликатиметься
    LOGIN_C = 0.5
    SIGNUP_C = 0.5
    SET_C = 1
    GET_C = 98

    TEST_EMAIL = 'test'
    TEST_PASS = 'test'
    TEST_TOKEN = ''

    @property
    def __header(self):
        return {"Content-Type": "application/json",
                "Authorization": f"Bearer {self.TEST_TOKEN}"}

    def __init__(self, url):
        self._URL = url

    def __setup(self):
        requests.post(f"{self._URL}/users/signup", headers=HEADERS,
                      data=json.dumps({"email": self.TEST_EMAIL, "password": self.TEST_PASS}))
        resp = requests.post(f"{self._URL}/users/signin", headers=HEADERS,
                      data=json.dumps({"email": self.TEST_EMAIL, "password": self.TEST_PASS}))
        logger.info(resp.text)
        token = resp.json()["access_token"]
        self.TEST_TOKEN = token
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {token}"}
        requests.post(f"{self._URL}/urls/shorten", headers=headers,
                      data=json.dumps({"url": "https://google.com"}))

    def __login(self, url):
        response = requests.post(f"{url}/", headers=HEADERS)
        return response

    def __signup(self, url):
        response = requests.post(f"{url}/", headers=HEADERS)
        return response

    def __set_shrtnr(self, url):
        random_url = random.choice(''.join(
            random.choice(string.ascii_letters) for i in range(10)
        ))
        response = requests.post(f"{url}/urls/shorten", headers=self.__header,
                                 data=json.dumps({"url": random_url}))
        return response

    def __get_shrtner(self, url):
        random_alias = random.choice(''.join(
            random.choice(string.ascii_letters) for i in range(10)
        ))
        response = requests.get(f"{url}/r/{random_alias}", allow_redirects=False)
        return response

    def _shoot(self, rand: List[float], qps: int, url: str, threads: int = 10) -> float:
        t_pause = 1 / qps * threads
        s = sum(rand)
        log = rand[0] / s
        reg = rand[1] / s + log
        get = rand[2] / s + reg
        set = rand[3] / s + get

        r = random.random()
        t_start = time.time()
        if r < log:
            resp = self.__login(url)
        elif r < reg:
            resp = self.__signup(url)
        elif r < get:
            resp = self.__get_shrtner(url)
        else:
            resp = self.__set_shrtnr(url)

        latency = time.time() - t_start
        if latency < t_pause:
            time.sleep(t_pause - latency)
        if resp.status_code < 500:
            return latency

    def start_shoot(self, qps, duration,
                    login=None,
                    sign_up=None,
                    get=None,
                    set=None,
                    threads: int = 10
                    ) -> List[float]:
        if any(map(lambda x: x is None, [login, sign_up, get, set])):
            login = self.LOGIN_C
            sign_up = self.SIGNUP_C
            get = self.GET_C
            set = self.SET_C
        random_api = [login, sign_up, get, set]

        with AppManager(self._URL):

            self.__setup()

            with ThreadPoolExecutor(threads) as executor:
                res = [executor.submit(self._shoot, random_api, qps, self._URL, threads)
                       for _ in range(qps*duration)]
                wait(res)
                latancies = [r.result() for r in res]

        return latancies


