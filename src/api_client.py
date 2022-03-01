import requests
import uuid


class ApiClient:
    def __init__(self, url: str, client_name: str):
        self._url = url
        self._client_name = client_name

        self._uuid: str = str(uuid.uuid4())
        self._password: str | None = None

    def get_active_tasks(self) -> list[str]:
        return requests.get(url=self._url + '/active-tasks').json()

    def submit_progress(self, processes_count: int, executed_tasks: dict):
        data = {
            'uuid': self._uuid,
            'readableName': self._client_name,
            'processesCount': processes_count,
            'executedTasks': list(
                dict({'ipAddressOrDomain': url, 'requestsCount': count}) for url, count in executed_tasks.items()),
        }

        if self._password is not None:
            data['password'] = self._password

        response = requests.post(url=self._url + '/submit-progress', json=data).json()

        if self._password is None:
            self._password = response['props']['password']

        return response
