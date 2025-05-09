import os
import pytest
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from alembic.config import Config
from alembic import command
from app.infrastructure.models import BaseModel
from app.infrastructure.utils.create_postgresql_database import create_if_not_exist_database
from dotenv import load_dotenv

os.environ["TEST_ENV"] = "true"
assert os.getenv("TEST_ENV") == "true"
dotenv_path = os.path.join(os.path.dirname(__file__), ".env.test")
load_dotenv(dotenv_path)

current_dir = os.path.dirname(os.path.abspath(__file__))
alembic_ini_path = os.path.join(current_dir, "alembic.ini")
migrations_path = os.path.join(current_dir, "migrations")


def create_test_database(database_url):
    create_if_not_exist_database(database_url)


def drop_test_database(database_url):
    """Удаляем тестовую базу данных."""
    engine = create_engine(database_url.rsplit("/", 1)[0] + "/postgres", isolation_level="AUTOCOMMIT")
    with engine.connect() as connection:
        # Принудительно завершаем все соединения с базой тестов
        connection.execute(text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='test_db'"))
        try:
            connection.execute(text("DROP DATABASE test_db"))
        except ProgrammingError:
            # Если база уже удалена или возникла иная ошибка, игнорируем её
            pass


@pytest.fixture(scope="session")
def test_db():
    """Фикстура для настройки базы данных на уровне всего сеанса тестов."""
    database_url = "postgresql+psycopg2://gorod:123qwe@localhost:5432/test_db"

    # Создаем базу, если еще не существует.
    create_test_database(database_url)

    # Применение миграций
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    alembic_cfg.set_main_option("script_location", migrations_path)  # при необходимости скорректируйте путь
    command.upgrade(alembic_cfg, "head")

    # Настраиваем подключение и создаем схемы
    engine = create_engine(database_url)
    BaseModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    yield Session, engine  # возвращаем сессию и двигатель для тестов

    # Очистка после завершения всех тестов
    engine.dispose()
    drop_test_database(database_url)


@pytest.fixture(scope="function")
def session(test_db):
    """Фикстура для отдельной сессии в каждом тесте."""
    Session, _ = test_db
    session = Session()
    # Применяем все изменения к базе
    connection = session.bind.connect()
    transaction = connection.begin()

    yield session  # Откатываем транзакцию только вручную после yield

    transaction.rollback()
    connection.close()
    session.close()


@pytest.fixture(scope="function")
def storage_factory(session):
    def _create_storage(storage_class):
        storage = storage_class()
        storage.engine = session.bind  # Привязываем движок базы из сессии
        storage.Session = lambda: session  # Привязываем сессию
        return storage

    return _create_storage


@pytest.fixture(scope="function")
def owner_id():
    return uuid.uuid4()
