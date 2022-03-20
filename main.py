import requests
from dotenv import load_dotenv


def get_vacancies(url, vacancy, area, period, page):
    url = url
    params = {'text': vacancy,
              'area': area,
              'period': period,
              'per_page': 100,
              'page': page,
              'only_with_salary': 'true'}
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
    count = 0
    while True:
        vacancies = get_vacancies('https://api.hh.ru/vacancies', 'Python', area_Moscow, 30, page)
        for vacancy in vacancies['items']:
            print(vacancy.get('name'), vacancy.get('salary'))
            count += 1
        page += 1
        print(f'Page: {page}, elements: {count}')
        if page == 20:
            break
    #have to check parameter 'found', 'pages', 'per_page', 'page' for counter control
    print(vacancies)


if __name__ == '__main__':
    main()
