from app.domain.lock_dto import LockCreateParams

from abc import ABC, abstractmethod
from typing import Optional


class ILockStorage(ABC):
    @abstractmethod
    async def lock(self, config: LockCreateParams) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def is_lock(self, lock_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, lock_id: str) -> None:
        raise NotImplementedError
