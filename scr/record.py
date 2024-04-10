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
    heat_number: int
    place: int | None
    athlete_id: int
    lane: int | None
    time: Decimal | None
    react_time: Decimal | None
    wind: str | None
    photo_file_name: str | None = None
    competition_id: int = 0

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
            int(fields[3]) if fields[3] else None,
            int(fields[4]),
            int(fields[5]) if fields[5] else None,
            _parse_time(fields[6]) if fields[6] else None,
            _parse_time(fields[7]) if fields[7] else None,
            fields[8] if fields[8] else None,
            fields[9] if fields[9] else None,
            int(fields[10]),
        )
        
def _parse_time(s):
    parts = s.split(":")
    if len(parts) == 1:
        return Decimal(parts[0])
    elif len(parts) == 2:
        return Decimal(int(parts[0]) * 60) + Decimal(parts[1])
    elif len(parts) == 3:
        return Decimal(int(parts[0]) * 3600) + Decimal(int(parts[1]) * 60) + Decimal(parts[2])
    else:
        raise ValueError(f"Invalid time format: {s}")



async def upsert_records(records: list[Record]):
    q = sa.text(UPSERT_QUERY)
    data = [r._asdict() for r in records]
    async with AsyncDbSession() as session:
        await session.execute(q, data)
        await session.commit()


UPSERT_QUERY = f"""
replace into {config.table_name} (event_number, round_number, heat_number, place, athlete_id, lane, time, react_time, wind, photo_file_name, competition_id)
values (:event_number, :round_number, :heat_number, :place, :athlete_id, :lane, :time, :react_time, :wind, :photo_file_name, :competition_id)
"""
