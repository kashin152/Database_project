from typing import Any

import psycopg2


def create_database(name, params):
    """
    Создание базы данных и таблиц для сохранения данных о вакансиях и о работодателях
    """
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {name}")
    cur.execute(f"CREATE DATABASE {name}")

    conn.close()

    conn = psycopg2.connect(database=name, **params)
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS company (
                company_id INT PRIMARY KEY,
                company_name VARCHAR,
                company_url TEXT
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES company(company_id),
                company_name VARCHAR,
                job_title TEXT,
                vacancy_url TEXT,
                salary_from INTEGER DEFAULT NULL,
                salary_to INTEGER DEFAULT NULL,
                currency TEXT DEFAULT NULL,
                description TEXT,
                requirement TEXT
            )
        """
        )

    conn.commit()
    conn.close()
    return "База данных и таблицы успешно созданы."


def save_data_to_database(
    data: list[dict[str, Any]],
    data_company: list[dict[str, Any]],
    database,
    params: dict,
):
    """
    Сохранение данных о работодателях и вакансиях в базу данных
    """
    conn = psycopg2.connect(dbname=database, **params)

    with conn.cursor() as cur:
        for company in data_company:
            cur.execute(
                """
            INSERT INTO company (company_id, company_name, company_url)
            VALUES (%s, %s, %s)
            """,
                (company["id"], company["name"], company["url"]),
            )
        for company in data:
            cur.execute(
                """
            INSERT INTO vacancies (company_id, company_name, job_title, vacancy_url, salary_from,
            salary_to, currency, description, requirement)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    company["company_id"],
                    company["company_name"],
                    company["job_title"],
                    company["link_to_vacancy"],
                    company["salary_from"],
                    company["salary_to"],
                    company["currency"],
                    company["description"],
                    company["requirement"],
                ),
            )

        conn.commit()
        conn.close()
    return "Таблицы успешно заполнены."
