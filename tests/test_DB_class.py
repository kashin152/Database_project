from src.config import config
from src.DB_class import DBManager

params = config(filename="database_test.ini", section="postgresql")
prog = DBManager("vacancy", params)


def test_prog_get_companies_and_vacancies_count():
    answer = prog.get_companies_and_vacancies_count()
    assert len(answer) == 15


def test_prog_get_all_vacancies():
    answer = prog.get_all_vacancies()
    assert answer is not None


def test_prog_get_avg_salary():
    answer = prog.get_avg_salary()
    assert answer != 1156
