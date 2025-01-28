import requests
from datetime import datetime, timedelta, timezone

class Response:
    def __init__(self, url):
        self._start_time = None
        self._server_time = None
        self._time_zone = None
        self._delta = None
        self._url = url

    def get_delta(self):
        return self._delta

    def get_response(self):
        self.set_start_time()
        response = requests.get(self._url)
        if response.status_code == 200:
            self.set_server_time(response)
            self.set_delta()
        else:
            raise Exception(f'Received status code: {response.status_code}')

    def set_start_time(self):
        self._start_time = datetime.now(timezone.utc)

    def set_server_time(self, resp):
        data = resp.headers['Date']
        date_format = "%a, %d %b %Y %H:%M:%S GMT"
        self._server_time = datetime.strptime(data, date_format).replace(tzinfo=timezone.utc)

    def set_delta(self):
        self._delta = abs(self._server_time - self._start_time)


if __name__ == "__main__":
    current_url = "https://yandex.com/time/sync.json?geo=213"

    deltas = []

    for i in range(5):
        response = Response(current_url)
        response.get_response()
        delta = response.get_delta()
        deltas.append(delta.total_seconds())

    if deltas:
        average_delta = sum(deltas) / len(deltas)
        print(f"Среднее арифметическое дельт: {average_delta} секунд")
    else:
        print("Массив deltas пустой")