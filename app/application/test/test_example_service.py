from unittest import TestCase
from unittest.mock import MagicMock
from uuid import uuid4

from app.constants import ExampleStatus
from app.domain.example_dto import ExampleDto, ExampleCreateParams
from app.application.example_service import ExampleService


class TestExampleService(TestCase):
    def setUp(self):
        self.storage_mock = MagicMock()
        self.service = ExampleService()
        self.service.storage = self.storage_mock

    async def test_get_returns_dto_when_example_exists(self):
        example_id = uuid4()
        expected_example = ExampleDto(id=example_id, status=ExampleStatus.active)
        self.storage_mock.get = MagicMock(return_value=expected_example)

        result = await self.service.get(example_id)

        self.assertEqual(result, expected_example)
        self.storage_mock.get.assert_called_once_with(example_id)

    async def test_get_returns_none_when_example_not_exists(self):
        example_id = uuid4()
        self.storage_mock.get = MagicMock(return_value=None)

        result = await self.service.get(example_id)

        self.assertIsNone(result)
        self.storage_mock.get.assert_called_once_with(example_id)

    async def test_get_or_fail_returns_dto_when_example_exists(self):
        example_id = uuid4()
        expected_example = ExampleDto(id=example_id, status=ExampleStatus.active)
        self.storage_mock.get = MagicMock(return_value=expected_example)

        result = await self.service.get_or_fail(example_id)

        self.assertEqual(result, expected_example)
        self.storage_mock.get.assert_called_once_with(example_id)

    async def test_get_or_fail_raises_error_when_example_not_exists(self):
        example_id = uuid4()
        self.storage_mock.get = MagicMock(return_value=None)

        with self.assertRaises(ValueError) as context:
            await self.service.get_or_fail(example_id)

        self.assertEqual(str(context.exception), f"Example with id {example_id} not found")
        self.storage_mock.get.assert_called_once_with(example_id)

    async def test_create_calls_storage_add(self):
        example_id = uuid4()
        params = ExampleCreateParams(id=example_id, status=ExampleStatus.active)
        self.storage_mock.add = MagicMock()

        await self.service.create(params)
        self.storage_mock.add.assert_called_once_with(params)
