import psycopg2


class DBManager:

    def __init__(self, dbname, params):
        self.dbname = dbname
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """SELECT company_name, COUNT(*) FROM vacancies GROUP BY company_name"""
        self.cur.execute(query)
        return {row[0]: row[1] for row in self.cur.fetchall()}

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        query = """
                SELECT job_title, company_name, salary_from, salary_to, currency, vacancy_url FROM vacancies
                """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """

        query = """
        SELECT AVG(salary_from) FROM vacancies WHERE currency = 'RUR'
        """
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """

        query = """
        SELECT company_name, job_title, salary_from, salary_to, vacancy_url FROM vacancies
        WHERE currency = 'RUR' and salary_from > (SELECT AVG(salary_from) FROM vacancies)
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """

        query = """
        SELECT * FROM vacancies
        WHERE LOWER(job_title) LIKE %s
        """
        self.cur.execute(query, ("%" + keyword.lower() + "%",))
        return self.cur.fetchall()
