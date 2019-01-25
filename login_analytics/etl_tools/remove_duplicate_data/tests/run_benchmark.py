# -*- coding: utf-8 -*-

import pandas as pd
from sfm.timer import Timer
from sqlalchemy_mate import engine_creator
from sqlalchemy_mate.crud.selecting import count_row
from sqlalchemy import select, func, text

from .db import metadata, t_events, t_temp_events_duplicate_ids, t_temp_events_distinct
from .test_data import create_test_data


class Config:
    host = "localhost"
    port = 5432
    username = "sanhehu"
    password = None
    database = "test"


engine = engine_creator.create_postgresql_psycopg2(
    host=Config.host,
    port=Config.port,
    username=Config.username,
    password=Config.password,
    database=Config.database,
)
metadata.create_all(engine)


def run():
    df_profiler = list()

    n_event_list = [
        1000,
        10000,
        100000,
        1000000,
    ]
    for n_event in n_event_list:
        duplicate_perc = 0.1
        start = "2018-01-01"
        end = "2018-12-31 23:59:59"

        n_dupes = int(n_event * duplicate_perc)

        with Timer(title="create test data"):
            t_event_data = create_test_data(
                n_event=n_event,
                duplicate_perc=duplicate_perc,
                start=start,
                end=end,
            )

        engine.execute(t_events.delete())
        with Timer(title="insert test data"):
            engine.execute(t_events.insert(), t_event_data)
            assert engine.execute(select([func.count(t_events.c.id)])).fetchone()[0] > n_event

        engine.execute(t_temp_events_duplicate_ids.delete())
        engine.execute(t_temp_events_distinct.delete())

        with Timer(title="remove duplicate") as timer:
            # First identify all the rows that are duplicate
            sql = text("""
            INSERT INTO temp_events_duplicate_ids (id)
            (
                SELECT events.id as id
                FROM events
                WHERE events.time BETWEEN '2018-01-01' AND '2018-12-31 23:59:59'
                GROUP BY id
                HAVING COUNT(*) > 1
            );
            """.strip())
            engine.execute(sql)

            # Extract one copy of all the duplicate rows

            sql = text("""
            INSERT INTO temp_events_distinct
            (
                SELECT DISTINCT *
                FROM events
                WHERE
                    events.time BETWEEN '2018-01-01' AND '2018-12-31 23:59:59'
                    AND events.id IN(
                        SELECT temp_events_duplicate_ids.id
                        FROM temp_events_duplicate_ids
                    )
            );
            """.strip())
            engine.execute(sql)

            # Remove all rows that were duplicated (all copies).
            sql = text("""
            DELETE
            FROM events
            WHERE
                events.time BETWEEN '2018-01-01' AND '2018-12-31 23:59:59'
                AND events.id IN(
                    SELECT temp_events_duplicate_ids.id
                    FROM temp_events_duplicate_ids
                );
            """.strip())
            engine.execute(sql)

            # Insert back in the single copies
            sql = text("""
            INSERT INTO events
            SELECT *
            FROM temp_events_distinct;
            """)
            engine.execute(sql)

            assert count_row(engine, t_events) == n_event
            assert count_row(engine, t_temp_events_duplicate_ids) == n_dupes
            assert count_row(engine, t_temp_events_distinct) == n_dupes

        df_profiler.append((n_event, n_dupes, timer.elapsed))

    df_profiler = pd.DataFrame(df_profiler, columns="n_event,n_dupe,time".split(","))
    print(df_profiler)
