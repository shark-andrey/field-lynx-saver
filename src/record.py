from __future__ import annotations
import sqlalchemy as sa
from sqlalchemy import text
import typing
from sqlalchemy.dialects.mysql import insert
from decimal import Decimal
from .db import AsyncDbSession
from .logger import logger
from . import config

class Record(typing.NamedTuple):
    event_number: int
    round_number: int
    flight_number: int
    place: int
    attempt: int
    athlete_id: int
    mark: Decimal
    wind: str | None
    photo: str | None = None
    
    @classmethod
    def parse(cls, text: str) -> list[Record]:
        str_records = text.split(";")
        str_records = [s.strip() for s in str_records]
        str_records = [s for s in str_records if len(s) > 0]
        records = []
        for s in str_records:
            try:
                record = cls._parse_record(s)
                records.append(record)
            except Exception as e:
                logger.exception(e)
        return records

    @classmethod
    def _parse_record(cls, text: str) -> Record:
        fields = [f.strip() for f in text.split(",")]
        if len(fields) < 8:
            raise ValueError(f"Not enough fields in record: {text!r}")

        def to_decimal_or_none(value: str | None) -> Decimal | None:
            if not value:
                return None
            try:
                return Decimal(value)
            except InvalidOperation:
                raise ValueError(f"Invalid decimal value: {value!r}")

        return cls(
            int(fields[0]),
            int(fields[1]),
            int(fields[2]),
            int(fields[3]),
            int(fields[4]),
            int(fields[5]),
            to_decimal_or_none(fields[6]),
            fields[7] or None,
            fields[8] if len(fields) > 8 else None,
        )
       

async def upsert_records(records: list[Record]):
    if not records:
        return

    q = text(UPSERT_QUERY)  # Используем text() вместо sa.text() для чистоты, хотя это одно и то же
    data = [r._asdict() for r in records]
    
    logger.debug(f"Preparing to upsert {len(records)} records")

    async with AsyncDbSession() as session:
        # 1. Явно начинаем транзакцию
        await session.begin()
        
        try:
            # 2. Получаем низкоуровневое соединение
            conn = await session.connection()
            
            # 3. Выполняем запрос напрямую через соединение.
            # asyncmy корректно обработает список словарей как executemany
            await conn.execute(q, data)
            
            # 4. Явно фиксируем транзакцию (это критически важно!)
            await session.commit()
            logger.info(f"Successfully upserted {len(records)} records.")
            
        except DBAPIError as e:
            # ЛОВИМ ОШИБКУ ДРАЙВЕРА (MySQL error)
            await session.rollback()
            logger.error(f"MySQL Error during upsert: {e.orig}") # e.orig содержит чистую ошибку MySQL
            logger.error(f"Query details: {q.text}")
            raise
        except Exception as e:
            await session.rollback()
            logger.exception(f"Unexpected error during upsert")
            raise

UPSERT_QUERY = f"""
replace into {config.table_name} (event_number, round_number, flight_number, place, attempt, athlete_id, mark, wind, photo)
values (:event_number, :round_number, :flight_number, :place, :attempt, :athlete_id, :mark, :wind, :photo)
"""
