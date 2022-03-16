import requests
from dotenv import load_dotenv


def get_positions(url, position):
    url = url
    params = {'text': position}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_areas(url, area):
    url = url
    params = {'text': area}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    print(get_positions('https://api.hh.ru/suggests/positions', 'Программист'))
    print(get_areas('https://api.hh.ru/suggests/areas', 'Москва'))
    return


if __name__ == '__main__':
    main()
