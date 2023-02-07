import asyncio

from db.cruds import user_application_key


async def update_key():
    while True:
        key = user_application_key.create_key()
        print(key)
        await asyncio.sleep(60 * 60 * 24)


executable_functions = [
    update_key
]
