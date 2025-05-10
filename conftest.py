import os
import pytest
import uuid
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import ProgrammingError
from alembic.config import Config
from alembic import command
from app.infrastructure.models import BaseModel
from app.infrastructure.utils.create_postgresql_database import create_if_not_exist_database
from dotenv import load_dotenv
import pytest_asyncio


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
    # For migrations and schema creation we use sync engine
    sync_database_url = "postgresql+psycopg2://gorod:123qwe@localhost:5432/test_db"

    # Создаем базу, если еще не существует.
    create_test_database(sync_database_url)

    # Применение миграций
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", sync_database_url)
    alembic_cfg.set_main_option("script_location", migrations_path)  # при необходимости скорректируйте путь
    command.upgrade(alembic_cfg, "head")

    # Настраиваем подключение и создаем схемы (sync for setup)
    sync_engine = create_engine(sync_database_url)
    BaseModel.metadata.create_all(sync_engine)

    yield sync_database_url  # возвращаем URL для создания async engine в async fixture

    # Очистка после завершения всех тестов
    sync_engine.dispose()
    drop_test_database(sync_database_url)


@pytest_asyncio.fixture(scope="function")
async def async_test_db(test_db):
    """Async fixture for database setup."""
    # Convert sync URL to async URL
    sync_database_url = test_db
    async_database_url = sync_database_url.replace("postgresql+psycopg2", "postgresql+asyncpg")

    async_engine = create_async_engine(async_database_url, pool_pre_ping=True, pool_recycle=3600)
    AsyncSession = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        # class_=AsyncSession
    )

    try:
        yield AsyncSession, async_engine
    finally:
        await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(async_test_db):
    AsyncSession, async_engine = async_test_db
    async_session = AsyncSession()

    try:
        yield async_session
        await async_session.commit()
    except Exception:
        await async_session.rollback()
        raise
    finally:
        await async_session.close()
        await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def storage_factory(session):
    def _create_storage(storage_class):
        storage = storage_class()

        def session_factory(**kwargs):
            if "bind" in kwargs:
                return session
            return session

        storage._BaseStorage__Session = session_factory
        return storage

    try:
        yield _create_storage
    finally:
        pass


@pytest.fixture(scope="function")
def owner_id():
    return uuid.uuid4()
