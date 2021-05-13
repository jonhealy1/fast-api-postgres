import os

from databases import Database
from geoalchemy2 import Geometry
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("geometry", Geometry("POLYGON")),
    Column("data", JSONB),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# databases query builder
database = Database(DATABASE_URL)
