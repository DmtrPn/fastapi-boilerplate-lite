import pytest
import uuid
from app.infrastructure.lock_storage import LockStorage, LockCreateParams


@pytest.fixture(scope="function")
def storage(storage_factory):
    return storage_factory(LockStorage)


async def test_add_lock(storage):
    lock_id = str(uuid.uuid4())
    config = LockCreateParams(lock_id=lock_id)

    result = await storage.lock(config)

    assert result == lock_id

    is_lock = await storage.is_lock(lock_id)
    assert is_lock is True


async def test_add_existing_lock(storage):
    lock_id = str(uuid.uuid4())
    config = LockCreateParams(lock_id=lock_id)

    await storage.lock(config)
    result = await storage.lock(config)

    assert result is None

    is_lock = await storage.is_lock(lock_id)
    assert is_lock is True


async def test_remove_lock(storage):
    lock_id = str(uuid.uuid4())
    config = LockCreateParams(lock_id=lock_id)

    await storage.lock(config)
    await storage.remove(lock_id)

    is_lock = await storage.is_lock(lock_id)
    assert is_lock is False
