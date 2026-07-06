from __future__ import annotations

import sqlalchemy as sa
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.dialects.mysql import insert
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
    wind: Optional[str]
    photo: Optional[str] = None

    @classmethod
    def parse(cls, text: str) -> List["Record"]:
        str_records = text.split(";")
        str_records = [s.strip() for s in str_records]
        str_records = [s for s in str_records if len(s) > 0]

        records: List["Record"] = []
        for s in str_records:
            try:
                record = cls._parse_record(s)
                records.append(record)
            except Exception as e:
                logger.exception(e)
        return records

    @classmethod
    def _parse_record(cls, text: str) -> "Record":
        fields = [f.strip() for f in text.split(",")]
        if len(fields) < 8:
            raise ValueError(f"Not enough fields in record: {text!r}")

        # Парсим поля в нужном порядке и типах
        event_number = int(fields[0])
        round_number = int(fields[1])
        flight_number = int(fields[2])
        place = int(fields[3])
        attempt = int(fields[4])
        athlete_id = int(fields[5])
        mark_str = fields[6]
        mark = Decimal(mark_str) if mark_str else Decimal("0")
        wind = fields[7] if len(fields) > 7 and fields[7] else None
        photo = fields[8] if len(fields) > 8 and fields[8] else None

        return cls(
            event_number=event_number,
            round_number=round_number,
            flight_number=flight_number,
            place=place,
            attempt=attempt,
            athlete_id=athlete_id,
            mark=mark,
            wind=wind,
            photo=photo,
        )


async def upsert_records(records: List[Record]):
    q = sa.text(UPSERT_QUERY)
    data = [r._asdict() for r in records]
    async with AsyncDbSession() as session:
        await session.execute(q, data)
        await session.commit()


UPSERT_QUERY = f"""
REPLACE INTO {config.table_name} (
    event_number, round_number, flight_number, place, attempt, athlete_id, mark, wind, photo
) VALUES (
    :event_number, :round_number, :flight_number, :place, :attempt, :athlete_id, :mark, :wind, :photo
)
"""
