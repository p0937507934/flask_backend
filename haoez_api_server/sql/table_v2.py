from sqlalchemy import (
    Column,
    Table,
    Integer,
    Float,
    VARCHAR,
    DateTime,
    ForeignKey,
    MetaData,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base


def keylist(metadata):
    return Table(
        "keylist",
        metadata,
        Column("Keylist_id", Integer, primary_key=True, nullable=False),
        Column("Camera_name", VARCHAR(20), nullable=False),
        Column("File_name", VARCHAR(50), nullable=False),
        Column("File_path", VARCHAR(50), nullable=False),
        Column("Sample_name", VARCHAR(50), nullable=False),
        Column("Sample_time",TIMESTAMP(),nullable=False),
        extend_existing=True,
    )
