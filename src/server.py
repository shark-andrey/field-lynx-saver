import asyncio
import traceback

from .record import Record, upsert_records
from .logger import logger
from . import config
from .db import init_db


async def main():
    await init_db()
    server = await asyncio.start_server(
        client_connected_cb=on_accept,
        host="0.0.0.0",
        port=config.port,
        reuse_address=True,
    )
    async with server:
        await server.serve_forever()


async def on_accept(reader, writer):
    logger.debug("Got connection")
    while True:
        message = await reader.readline()
        if message == b"":
            break
        try:
            message = message.decode().strip()
        except UnicodeDecodeError:
            logger.error("Error decoding message: {message}")
            continue
        if len(message) > 0:
            logger.debug(f"Message: {message}")
            try:
                await handle_message(message)
            except Exception as e:
                logger.exception(e)


async def handle_message(message: str):
    records: list[Record] = Record.parse(message)
    if len(records) > 0:
        logger.debug(f"Upserting {len(records)} records")
        await upsert_records(records)


if __name__ == "__main__":
    asyncio.run(main())
