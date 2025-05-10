from sqlalchemy.sql import text, exists, select
from sqlalchemy import delete

from app.application.abastract.i_lock_storage import ILockStorage, LockCreateParams
from app.infrastructure.abstract.base_storage import BaseStorage
from app.infrastructure.models.lock_model import LockModel
from typing import Optional
from datetime import datetime, timedelta, timezone


class LockStorage(ILockStorage, BaseStorage):
    async def lock(self, config: LockCreateParams) -> Optional[str]:
        async with self.session_scope() as session:
            expiration_time = datetime.now(timezone.utc) - timedelta(minutes=5)
            delete_query = text("DELETE FROM lock WHERE lock_id = :lock_id AND created_at < :expiration_time")
            await session.execute(delete_query, {"expiration_time": expiration_time, "lock_id": str(config.lock_id)})

            query = text(
                """INSERT INTO lock (lock_id, created_at)
                   VALUES (:lock_id, now()) ON CONFLICT (lock_id) DO NOTHING
                                          RETURNING lock_id"""
            )
            result = await session.execute(query, {"lock_id": str(config.lock_id)})
            return result.scalar()

    async def is_lock(self, lock_id: str) -> bool:
        async with self.session_scope(read_only=True) as session:
            query = select(exists().where(LockModel.lock_id == lock_id))
            result = await session.execute(query)
            return result.scalar()

    async def remove(self, lock_id: str) -> None:
        async with self.session_scope() as session:
            query = delete(LockModel).where(LockModel.lock_id == lock_id)
            await session.execute(query)
