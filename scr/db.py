import sqlalchemy as sa
import asyncio
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from . import config

async_engine = create_async_engine(config.db_url)
AsyncDbSession = sessionmaker(async_engine, class_=AsyncSession)


async def init_db():
    query_path = os.path.abspath(f"{__file__}/../init.sql")
    with open(query_path, "r") as f:
        query = f.read()
    query = query.replace("TABLE_NAME", config.table_name)
    async with AsyncDbSession() as session:
        await session.execute(sa.text(query))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(init_db())
