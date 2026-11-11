import asyncio
import threading
import pytest
from app import add_note, calculate_in_thread, future_error, future_value, get_todo


@pytest.mark.asyncio
async def test_future_returns_expected_value():
    result = await future_value()
    assert result == "готово"

@pytest.mark.asyncio
async def test_future_raises_expected_error():
    with pytest.raises(ValueError, match="ошибка"):
        await future_error()

@pytest.mark.asyncio
async def test_http_request_returns_todo():
    todo = await get_todo(1)
    assert todo["id"] == 1
    assert isinstance(todo["title"], str)
    assert todo["title"]

@pytest.mark.asyncio
async def test_database_saves_note():
    result = await add_note("проверка")
    assert result == "проверка"

@pytest.mark.asyncio
async def test_async_function_runs_in_thread():
    main_thread_id = threading.get_ident()
    result_thread_id = await calculate_in_thread()
    assert result_thread_id != main_thread_id