import requests
from dotenv import load_dotenv


def get_role(text):
    url = 'https://api.hh.ru/suggests/professional_roles'
    params = {'text': text}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items'][0]['id']


def get_vacancies(role, language, area, period, page):
    url = 'https://api.hh.ru/vacancies'
    params = {'text': language,
              'area': area,
              'period': period,
              'per_page': 100,
              'page': page,
              'only_with_salary': 'true',
              'professional_role': role}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def hh_analyze(languages):
    page = 0
    count = 0
    count_language = 0
    try:
        while True:
            vacancies = get_vacancies(get_role('Программист'), languages[count_language], 1, 3, page)
            for vacancy in vacancies['items']:
                print(vacancy.get('name'), vacancy.get('salary'))
                count += 1
            page += 1
            print(f'Page: {page}, elements: {count}, {languages[count_language]}')
            if page == vacancies['pages']:
                count_language += 1
                page = 0
                count = 0
    except IndexError:
        return



def main():
    load_dotenv()
    languages = ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    hh_analyze(languages)


if __name__ == '__main__':
    main()
