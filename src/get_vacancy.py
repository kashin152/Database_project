import requests


def get_company():
    """
    Получаем 15 работодателей с HH.ру
    """
    url_hh = "https://api.hh.ru/vacancies"
    vacancies_hh = requests.get(
        url_hh, params={"currency": "RUR", "host": "hh.ru"}
    ).json()
    list_company = []
    for i in range(0, 100):
        if len(list_company) == 15:
            break
        elif {
            "id": vacancies_hh["items"][i]["employer"]["id"],
            "name": vacancies_hh["items"][i]["employer"]["name"],
            "url": vacancies_hh["items"][i]["employer"]["url"],
        } in list_company:
            continue
        else:
            list_company.append(
                {
                    "id": vacancies_hh["items"][i]["employer"]["id"],
                    "name": vacancies_hh["items"][i]["employer"]["name"],
                    "url": vacancies_hh["items"][i]["employer"]["url"],
                }
            )
    return list_company


def get_vacancies(list_company):
    """
    Выгружаем все вакансии, опубликованные компанией
    """

    vacancies_info = []
    for company in list_company:
        company_id = company["id"]
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json()["items"]
            vacancies_info.extend(vacancies)

        else:
            print(
                f"Ошибка при запросе к API для компании {company['company_name']}: {response.status_code}"
            )
    return vacancies_info


def get_vacancies_list(vacancies_info):
    """
    Получаем список словарей с данными для БД
    """
    vacancies_list = []
    for item in vacancies_info:
        company_id = item["employer"]["id"]
        company = item["employer"]["name"]
        company_url = item["employer"]["url"]
        job_title = item["name"]
        link_to_vacancy = item["employer"]["alternate_url"]
        try:
            salary_from = item["salary"]["from"]

        except KeyError:
            salary_from = 0

        try:
            salary_to = item["salary"]["to"]

        except KeyError:
            salary_to = 0

        try:
            currency = item["salary"]["currency"]

        except KeyError:
            currency = 0
        description = item["snippet"]["responsibility"]
        requirement = item["snippet"]["requirement"]
        vacancies_list.append(
            {
                "company_id": company_id,
                "company_name": company,
                "company_url": company_url,
                "job_title": job_title,
                "link_to_vacancy": link_to_vacancy,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "description": description,
                "requirement": requirement,
            }
        )
    return vacancies_list
