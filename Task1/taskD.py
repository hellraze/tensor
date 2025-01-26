import requests
from datetime import datetime, timedelta, timezone

class Response:
    def __init__(self, url):
        self.start_time = None
        self.server_time = None
        self.time_zone = None
        self.delta = None
        self.url = url

    def get_delta(self):
        return self.delta

    def get_response(self):
        self.set_start_time()
        # requesting url and return json dict if success or status code
        response = requests.get(self.url)
        if response.status_code == 200:
            self.set_server_time(response)
            self.set_delta()
        else:
            raise Exception(f'Received status code: {response.status_code}')

    def set_start_time(self):
        self.start_time = datetime.now(timezone.utc)

    def set_server_time(self, resp):
        self.set_time_zone(resp)

        data = resp.headers['Date']
        date_format = "%a, %d %b %Y %H:%M:%S GMT"
        date_object = datetime.strptime(data, date_format)

        utc_offset = timedelta(hours=self.time_zone)
        self.server_time = date_object.replace(tzinfo=timezone.utc).astimezone(timezone(utc_offset))

    def set_time_zone(self, resp):
        data = resp.json()
        time_zone_str = data['clocks']['213']['offsetString']
        differ_hours = time_zone_str.split(":")[0]
        hours = int(differ_hours[3:])
        self.time_zone = hours

    def set_delta(self):
        self.delta = self.start_time - self.server_time


if __name__ == "__main__":
    current_url = "https://yandex.com/time/sync.json?geo=213"

    deltas = []

    for i in range(5):
        response = Response(current_url)

        response.get_response()
        delta = response.get_delta()
        deltas.append(delta)

    for j in deltas:
        print(j)
