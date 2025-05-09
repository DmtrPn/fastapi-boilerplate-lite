from app.logger import logging

from sqlalchemy_utils import database_exists, create_database


def create_if_not_exist_database(url):
    if not database_exists(url):
        logging.info(f"База данных не существует. Создаём: {url}")
        create_database(url)
    else:
        logging.info(f"База {url} данных уже существует.")
