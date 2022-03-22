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


def main():
    load_dotenv()
    languages = ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    page = 0
    count = 0
    count_language = 0
    while True:
        vacancies = get_vacancies('https://api.hh.ru/vacancies', f'{languages[count_language]}', 1, 3, page)
        for vacancy in vacancies['items']:
            print(vacancy.get('name'), vacancy.get('salary'))
            count += 1
        page += 1
        print(f'Page: {page}, elements: {count}, {languages[count_language]}')
        if page == vacancies['pages']:
            count_language += 1
            page = 0
            count = 0




if __name__ == '__main__':
    main()
