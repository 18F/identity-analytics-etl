# -*- coding: utf-8 -*-

from sqlalchemy import MetaData, Table, Column
from sqlalchemy import String, DateTime

metadata = MetaData()

t_events = Table(
    "events", metadata,
    Column("id", String),
    Column("time", DateTime),
)

t_temp_events_duplicate_ids = Table(
    "temp_events_duplicate_ids", metadata,
    Column("id", String),
)

t_temp_events_distinct = Table(
    "temp_events_distinct", metadata,
    Column("id", String),
    Column("time", DateTime),
)
