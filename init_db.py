from app.infrastructure.utils.create_postgresql_database import create_if_not_exist_database
from app.config import settings


if __name__ == "__main__":
    # init_db()
    create_if_not_exist_database(settings.DATABASE_URI)
    print("Таблицы созданы!")
