from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional


@dataclass
class LockCreateParams:
    lock_id: str


class ILockService(ABC):
    @abstractmethod
    async def lock(self, lock_id: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    async def is_lock(self, lock_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, lock_id: str) -> None:
        raise NotImplementedError
