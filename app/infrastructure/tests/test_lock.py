import pytest
import uuid
from app.infrastructure.lock_storage import LockStorage, LockCreateParams


@pytest.fixture(scope="function")
def storage(storage_factory):
    return storage_factory(LockStorage)


def test_add_lock(storage, session):
    # Создаем конфигурацию для нового lock
    lock_id = str(uuid.uuid4())
    config = LockCreateParams(lock_id=lock_id)

    # Операция add
    result = storage.lock(config)

    # Если добавление прошло успешно, result должен быть равен lock_id
    assert result == lock_id

    is_lock = storage.is_lock(lock_id)
    assert is_lock is True


def test_add_existing_lock(storage, session):
    # Создаем конфигурацию для нового lock
    lock_id = str(uuid.uuid4())
    config = LockCreateParams(lock_id=lock_id)

    # Добавляем lock в первый раз
    storage.lock(config)

    # Добавляем lock во второй раз (конфликт)
    result = storage.lock(config)

    # Второй вызов должен вернуть None (lock уже существует)
    assert result is None

    is_lock = storage.is_lock(lock_id)
    assert is_lock is True


def test_remove_lock(storage, session):
    # Создаем конфигурацию для нового lock
    lock_id = str(uuid.uuid4())
    config = LockCreateParams(lock_id=lock_id)

    # Добавляем lock
    storage.lock(config)

    # Удаляем lock
    storage.remove(lock_id)

    # Проверяем, что lock удалён из базы
    is_lock = storage.is_lock(lock_id)
    assert is_lock is False
