import asyncio

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
    # Устройство разделяет записи символом ";" и не гарантирует перевод строки,
    # поэтому нельзя использовать reader.readline() - он будет копить данные в
    # буфере до "\n" или до разрыва соединения (это и была причина пакетной
    # записи только при закрытии сокета). Читаем сырые байты и режем по ";" сами.
    addr = writer.get_extra_info("peername")
    logger.debug(f"Got connection from {addr}")
    buffer = b""
    while True:
        chunk = await reader.read(4096)
        if chunk == b"":
            break
        buffer += chunk
        *complete, buffer = buffer.split(b";")
        for raw in complete:
            await _handle_raw(raw)
    if buffer.strip():
        await _handle_raw(buffer)
    logger.debug(f"Connection closed by {addr}")


async def _handle_raw(raw: bytes):
    try:
        message = raw.decode().strip()
    except UnicodeDecodeError:
        logger.error(f"Error decoding message: {raw!r}")
        return
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
