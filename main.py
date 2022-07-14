import os

import requests
from collections import Counter
from dotenv import load_dotenv


# from dotenv import load_dotenv

# get role ID for requested vacancy
def get_role(text):
    url = 'https://api.hh.ru/suggests/professional_roles'
    params = {'text': text}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items'][0]['id']


# get filtered vacancies
def get_vacancies(role, language, area, period, page):
    url = 'https://api.hh.ru/vacancies'
    params = {'text': language,
              'area': area,
              'period': period,
              'per_page': 100,
              'page': page,
              'only_with_salary': 'true',
              'currency': 'RUR',
              'professional_role': role}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def predict_rub_salary(vacancy):
    if vacancy['currency'] != 'RUR':
        result = None
    elif vacancy['from'] and vacancy['to']:
        result = (int(vacancy['from']) + int(vacancy['to'])) / 2
    elif not vacancy['to']:
        result = (int(vacancy['from'])) * 1.2
    elif not vacancy['from']:
        result = (int(vacancy['to'])) * 0.8
    return result


def get_raw_hh(languages):
    page, count, count_language = 0, 0, 0
    output = {}
    try:
        while True:
            vacancies = get_vacancies(get_role('Программист'), languages[count_language], 1, 1, page)
            for vacancy in vacancies['items']:
                output[languages[count_language], count] = vacancy.get('salary')
                count += 1
            page += 1
            if page == vacancies['pages']:
                count_language += 1
                page, count = 0, 0
    except IndexError:
        return output


def get_filtered_hh():
    lang_salary, none_results = {}, []
    languages = ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    for lang_num, salary in get_raw_hh(languages).items():
        result_salary = predict_rub_salary(salary)
        if result_salary is None:
            none_results.append(lang_num[0])
        if lang_num[0] not in lang_salary.keys():
            lang_salary[lang_num[0]] = {'sum_salary': int(result_salary or 0), 'total_vacancies': lang_num[1] + 1}
        else:
            lang_salary[lang_num[0]]['sum_salary'] += int(result_salary or 0)
            lang_salary[lang_num[0]]['total_vacancies'] = lang_num[1] + 1
        lang_salary[lang_num[0]]['none'] = dict(Counter(none_results)).get(lang_num[0])
        lang_salary[lang_num[0]]['processed_vacancies'] = lang_salary[lang_num[0]]['total_vacancies'] - int(
            lang_salary[lang_num[0]]['none'] or 0)
        lang_salary[lang_num[0]]['mean_salary'] = lang_salary[lang_num[0]]['sum_salary'] / (
                    lang_salary[lang_num[0]]['processed_vacancies'] or 1)
    return lang_salary


def get_superjob(token, keyword):
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {'X-Api-App-Id': token}
    params = {'keyword': keyword}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    superjob_token = os.getenv('SUPERJOBTOKEN')
    print(get_filtered_hh())
    print(get_superjob(superjob_token, 'Программист'))


if __name__ == '__main__':
    main()
