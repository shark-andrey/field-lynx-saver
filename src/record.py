from __future__ import annotations

import sqlalchemy as sa
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
        event_number=int(fields[0]),
        round_number=int(fields[1]),
        flight_number=int(fields[2]),
        place=int(fields[3]),
        attempt=int(fields[4]),
        athlete_id=int(fields[5]),
        mark=to_decimal_or_none(fields[6]),
        wind=fields[7] or None,
        photo_file_name=fields[8] if len(fields) > 8 else None,
        )
        

async def upsert_records(records: list[Record]):
    q = sa.text(UPSERT_QUERY)
    data = [r._asdict() for r in records]
    async with AsyncDbSession() as session:
        await session.execute(q, data)
        await session.commit()


UPSERT_QUERY = f"""
replace into {config.table_name} (event_number, round_number, flight_number, place, attempt, athlete_id, mark, wind, photo)
values (:event_number, :round_number, :flight_number, :place, :attempt, :athlete_id, :mark, :wind, :photo)
"""
