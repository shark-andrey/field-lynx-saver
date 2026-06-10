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
        fields = text.split(",")
        return cls(
            int(fields[0]),
            int(fields[1]),
            int(fields[2]),
            int(fields[3]),
            int(fields[4]),
            int(fields[5]),
            fields[6] if fields[6] else None,
            fields[7] if fields[7] else None,
        )
        

async def upsert_records(records: list[Record]):
    q = sa.text(UPSERT_QUERY)
    data = [r._asdict() for r in records]
    async with AsyncDbSession() as session:
        await session.execute(q, data)
        await session.commit()


UPSERT_QUERY = f"""
replace into {config.table_name} (event_number, round_number, flight_number, place, attempt, athlete_id, mark, wind)
values (:event_number, :round_number, :flight_number, :place, :attempt, :athlete_id, :mark, :wind)
"""

