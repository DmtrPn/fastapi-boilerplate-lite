from sqlalchemy.sql import text

from app.application.abastract.i_lock_storage import ILockStorage, LockCreateParams
from app.infrastructure.abstract.base_storage import BaseStorage
from app.infrastructure.models.lock_model import LockModel
from typing import Optional
from datetime import datetime, timedelta, timezone


class LockStorage(ILockStorage, BaseStorage):
    def lock(self, config: LockCreateParams) -> Optional[str]:
        with self.session_scope() as session:
            expiration_time = datetime.now(timezone.utc) - timedelta(minutes=5)
            delete_query = text("DELETE FROM lock WHERE lock_id = :lock_id AND created_at < :expiration_time")
            session.execute(delete_query, {"expiration_time": expiration_time, "lock_id": str(config.lock_id)})

            query = text(
                """INSERT INTO lock (lock_id, created_at)
                   VALUES (:lock_id, now()) ON CONFLICT (lock_id) DO NOTHING
                                       RETURNING lock_id"""
            )
            result = session.execute(query, {"lock_id": str(config.lock_id)})
            # Если вставка успешна, будет возвращён lock_id, иначе None
            return result.scalar()

    def is_lock(self, lock_id: str) -> bool:
        with self.session_scope(read_only=True) as session:
            query = session.query(LockModel).filter(LockModel.lock_id == lock_id).exists()
            return session.query(query).scalar()

    def remove(self, lock_id: str) -> None:
        with self.session_scope() as session:
            session.query(LockModel).filter(LockModel.lock_id == lock_id).delete(synchronize_session="fetch")
