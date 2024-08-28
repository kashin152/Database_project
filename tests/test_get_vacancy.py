from src.get_vacancy import get_company, get_vacancies, get_vacancies_list

tes = get_company()
tes2 = get_vacancies(tes)
tes3 = get_vacancies_list(tes2)


def test_get_company():
    assert len(get_company()) == 15


def test_get_company_dete():
    tes = get_company()
    assert tes[1] == {
        "id": "756658",
        "name": "Фабрика мебельных деталей",
        "url": "https://api.hh.ru/employers/756658?host=hh.ru",
    }


def test_get_vacancies_list():
    assert get_vacancies_list(tes2) is not None
