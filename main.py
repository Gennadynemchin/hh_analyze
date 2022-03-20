import requests
from dotenv import load_dotenv


def get_vacancies(url, vacancy, area, period, page):
    url = url
    params = {'text': vacancy, 'area': area, 'period': period, 'per_page': 100, 'page': page}
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
    area_Moscow = get_areas('https://api.hh.ru/suggests/areas', 'Москва')['items'][0]['id']
    page = 0
    while True:
        try:
            vacancies = get_vacancies('https://api.hh.ru/vacancies', 'Python', area_Moscow, 1, page)
            count = 0
            for vacancy in vacancies['items']:
                print(vacancy['name'], vacancy['salary'])
                count += 1
            page += 1
            print(f'Page: {page}, elements: {count}')
        except requests.exceptions.HTTPError:
            break


if __name__ == '__main__':
    main()
