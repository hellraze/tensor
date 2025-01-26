import requests

def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f'Received status code: {response.status_code}')


if __name__ == "__main__":
    try:
        current_url = "https://yandex.com/time/sync.json?geo=213"
        result = get_response(current_url)
        print(result)
    except Exception as e:
        print("Exception occurred:", str(e))