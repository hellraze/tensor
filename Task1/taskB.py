import requests
import datetime

class Response:

    def __init__(self, url):
        self._time = None
        self._time_zone = None
        self._url = url

    def get_response(self):
        response = requests.get(self._url)
        if response.status_code == 200:
            data = response.json()
            self.set_time_and_time_zone(data)
        else:
            raise Exception(f'Received status code: {response.status_code}')

    def __str__(self):
        return f'{self._time} {self._time_zone}'

    def set_time_and_time_zone(self, data):
        self.set_time_zone(data["clocks"]["213"]["offsetString"])
        self.set_time_from_posix(data["time"])

    def set_time_zone(self, time_zone):
        self._time_zone = time_zone

    def set_time_from_posix(self, time):
        seconds = time / 1000
        data_time = datetime.datetime.fromtimestamp(seconds)
        self._time = data_time.strftime('%H:%M:%S')


if __name__ == "__main__":

    current_url = "https://yandex.com/time/sync.json?geo=213"
    response = Response(current_url)

    response.get_response()

    print(response)
