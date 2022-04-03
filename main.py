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
              'currency': 'RUR',
              'professional_role': role}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_from_hh(languages):
    page, count, count_language = 0, 0, 0
    output = {}
    try:
        while True:
            vacancies = get_vacancies(get_role('Программист'), languages[count_language], 1, 1, page)
            for vacancy in vacancies['items']:
                output[languages[count_language],count] = vacancy.get('salary')
                count += 1
            page += 1
            if page == vacancies['pages']:
                count_language += 1
                page, count = 0, 0
    except IndexError:
        return output


def predict_rub_salary(vacancy):
    if vacancy['currency'] != 'RUR':
        result = 0
    elif vacancy['from'] and vacancy['to']:
        result = (int(vacancy['from']) + int(vacancy['to'])) / 2
    elif not vacancy['to']:
        result = (int(vacancy['from'])) * 1.2
    elif not vacancy['from']:
        result = (int(vacancy['to'])) * 0.8
    return result


def main():
    load_dotenv()
    lang_salary = {}
    languages = ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    output_vacancies = get_from_hh(languages)
    for lang_num, salary in output_vacancies.items():
        language = lang_num[0]
        lang_count = lang_num[1] + 1
        result_salary = predict_rub_salary(salary)
        if language not in lang_salary.keys():
            lang_salary[language] = int(result_salary)
        else:
            lang_salary[language] = int(lang_salary[language]) + int(result_salary)
        print(language, lang_count)
    print(lang_salary)

if __name__ == '__main__':
    main()
