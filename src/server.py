import asyncio
import traceback

from .record import Record, upsert_records
from .logger import logger
from . import config
from .db import async_engine


async def main():
    # Проверка здоровья БД — оставляем, это полезно
    logger.info("Starting DB health check...")
    t0 = time.perf_counter()
    try:
        async with async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        t1 = time.perf_counter()
        logger.info(f"DB health check OK, took {t1 - t0:.3f}s")
    except Exception as e:
        logger.exception("DB health check failed")
        raise e
        
    server = await asyncio.start_server(
        client_connected_cb=on_accept,
        host="0.0.0.0",
        port=config.port,
        reuse_address=True,
    )
    logger.info(f"Server started on port {config.port}")
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
