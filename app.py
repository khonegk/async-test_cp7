import asyncio
import threading

import aiohttp
import aiosqlite


async def future_value():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    loop.call_soon(future.set_result, "готово")
    return await future


async def future_error():
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    loop.call_soon(future.set_exception, ValueError("ошибка"))
    return await future


async def get_todo(todo_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
        ) as response:
            response.raise_for_status()
            return await response.json()


async def add_note(text):
    async with aiosqlite.connect(":memory:") as db:
        await db.execute("CREATE TABLE notes (text TEXT)")
        await db.execute("INSERT INTO notes (text) VALUES (?)", (text,))
        await db.commit()
        async with db.execute("SELECT text FROM notes") as cursor:
            row = await cursor.fetchone()
    return row[0]


async def calculate_in_thread():
    async def calculation():
        await asyncio.sleep(0.01)
        return threading.get_ident()

    return await asyncio.to_thread(asyncio.run, calculation())