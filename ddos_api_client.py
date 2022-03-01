import requests
import uuid


class DdosApiClient:
    def __init__(self, url: str, client_name: str):
        self.url = url
        self.client_name = client_name

        self.uuid: str = str(uuid.uuid4())
        self.password: str | None = None

    def get_active_tasks(self):
        return requests.get(url=self.url + '/active-tasks').json()

    def submit_progress(self, processes_count: int, executed_tasks):
        data = {
            'uuid': self.uuid,
            'readableName': self.client_name,
            'processesCount': processes_count,
            'executedTasks': executed_tasks,
        }

        if self.password is not None:
            data['password'] = self.password

        response = requests.post(url=self.url + '/submit-progress', json=data).json()

        if self.password is None:
            self.password = response['props']['password']

        return response
