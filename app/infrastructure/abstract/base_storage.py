from abc import ABC
from app.infrastructure.config import get_session
from contextlib import contextmanager
from sqlalchemy.orm import Session


class BaseStorage(ABC):
    def __init__(self):
        self.__Session = get_session()

    @contextmanager
    def session_scope(self, read_only=False):
        session: Session = self.__Session()
        try:
            if read_only:
                session = self.__Session(
                    bind=session.bind.execution_options(isolation_level="AUTOCOMMIT")  # type: ignore
                )
            yield session
            if not read_only:
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
