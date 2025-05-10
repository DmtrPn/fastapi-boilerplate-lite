from app.application.abastract.i_lock_storage import ILockStorage
from app.domain.lock_dto import ILockService, LockCreateParams
from app.infrastructure.lock_storage import LockStorage
from typing import Optional


class LockService(ILockService):
    storage: ILockStorage = LockStorage()

    async def lock(self, lock_id: str) -> Optional[str]:
        return await self.storage.lock(LockCreateParams(lock_id=lock_id))

    async def is_lock(self, lock_id: str) -> bool:
        return await self.storage.is_lock(lock_id)

    async def remove(self, lock_id: str) -> None:
        await self.storage.remove(lock_id)
