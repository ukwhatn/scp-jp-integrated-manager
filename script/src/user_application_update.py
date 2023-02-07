import asyncio
import logging

from db.cruds import user_application_key

logger = logging.getLogger(__name__)


async def update_key():
    while True:
        logger.info("Checking keys...")
        key = user_application_key.create_key_if_expired()
        if key is not None:
            logger.info(f"Created new key: {key}")
        # 30分ごとにチェック
        await asyncio.sleep(60 * 30)


executable_functions = [
    update_key
]
