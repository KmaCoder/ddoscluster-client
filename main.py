from ddos_api_client import DdosApiClient
from args_util import get_arguments
from config import API_HOST

if __name__ == '__main__':
    args = get_arguments()
    api_instance = DdosApiClient(url=API_HOST, client_name=args.name)

    active_tasks = api_instance.get_active_tasks()
    print(active_tasks)

    progress_response = api_instance.submit_progress(processes_count=args.threads, executed_tasks=[])
    print(progress_response)
