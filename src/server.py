import asyncio
import time
from sqlalchemy import text

from .record import upsert_records
from .logger import logger
from . import config
from .db import async_engine  # оставляем только async_engine


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
    addr = writer.get_extra_info("peername")
    logger.debug(f"Got connection from {addr}")

    while True:
        try:
            message_bytes = await reader.readline()
        except Exception as e:
            logger.warning(f"Read error from {addr}: {e}")
            break

        if message_bytes == b"":
            logger.debug(f"Connection closed by {addr}")
            break

        message = None
        try:
            message = message_bytes.decode("utf-8").strip()
        except UnicodeDecodeError as e:
            # Исправлено: теперь реально подставляется значение ошибки и сырые данные
            logger.error(f"Unicode decode error from {addr}: {e}, raw={message_bytes!r}")
            continue

        if not message:
            continue

        logger.debug(f"Message: {message}")
        try:
            await handle_message(message)
        except Exception as e:
            logger.exception("Error handling message", exc_info=e)


async def handle_message(message: str):
    from .record import Record
    import time

    t0 = time.perf_counter()
    records = Record.parse(message)
    t1 = time.perf_counter()

    if not records:
        return

    logger.debug(f"Parsed {len(records)} records in {t1 - t0:.3f}s")

    t2 = time.perf_counter()
    await upsert_records(records)
    t3 = time.perf_counter()

    logger.info(
        f"Upsert {len(records)} records: parse={t1 - t0:.3f}s, db={t3 - t2:.3f}s"
    )


if __name__ == "__main__":
    asyncio.run(main())
