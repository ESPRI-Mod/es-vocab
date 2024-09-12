import sqlalchemy as sa
from sqlmodel import SQLModel, Field, select, cast, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

class UniverseTerm(SQLModel, table=True):

    __tablename__ = "universe_terms"

    pk: int | None = Field(default=None, primary_key=True)
    id: str
    json_content: dict = Field(sa_column=sa.Column(JSONB))

db_url = 'postgresql+asyncpg://postgres:mdpirulez@es-vocab-dev.ipsl.fr:5432/test'
engine = create_async_engine(db_url, echo=True)

async def create_tables():
    UniverseTerm.__table_args__ = (sa.Index('tmp_idx', UniverseTerm.__table__.c.json_content['name'], postgresql_using="gin"))
    UniverseTerm.__table_args__ = (sa.Index('json_content_idx', UniverseTerm.__table__.c.json_content['localisation']['city'], postgresql_using="gin"))
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
    

async def add_terms():
     async with AsyncSession(engine) as session:
        term_1 = UniverseTerm(id='ipsl', json_content={'localisation': {'city': 'Paris', 'gps': 0}, 'name': 'ipsl'})
        term_2 = UniverseTerm(id='dkrz', json_content={'localisation': {'city': 'Berlin', 'gps': 1}, 'name': 'dkrz'})
        session.add(term_1)
        session.add(term_2)
        await session.commit()

async def search():
     async with AsyncSession(engine) as session:
        #statement = select(UniverseTerm).where(cast(UniverseTerm.json_content['localisation']['gps'], Integer) == 1)
        #statement = select(UniverseTerm).where(cast(UniverseTerm.json_content['name'], String).contains("ipsl"))
        statement = select(UniverseTerm).where(UniverseTerm.json_content['name'].astext == 'ipsl')
        #print(statement.compile(dialect=postgresql.dialect()))
        results = await session.exec(statement)
        for result in results:
            print(result)

async def list_all():
     async with AsyncSession(engine) as session:
        statement = select(UniverseTerm)
        results = await session.exec(statement)
        for result in results:
            print(result)

#asyncio.run(create_tables())
#asyncio.run(add_terms())
asyncio.run(search())