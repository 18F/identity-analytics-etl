import json
import csv
import re
import io
import hashlib
import numpy as np
import os

# Try loading additional dependencies from tmp.

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

class Parser(object):
    header_fields = []

    def stream_csv(self, in_io):
        rows = 0
        out = io.StringIO()
        out_parquet = io.BytesIO()
        header_rows = [i for i in self.header_fields]
        df = pd.DataFrame(columns=header_rows)
        writer = csv.writer(out, delimiter=',')
        writer.writerow(header_rows)

        for line in in_io.decode('utf-8').split('\n'):
            if self.format_check(line):
                continue

            result, uuid = self.json_to_csv(self.extract_json(line))
            if uuid in self.uuids:
                continue

            self.uuids.add(uuid)
            writer.writerow(result)
            df.loc[len(df)] = result
            rows += 1

        # Pyarrow tries to infer types by default.
        # Explicitly set the types to prevent mis-typing.
        df = self.apply_df_types(df)

        # Convert pandas.DataFrame -> pyarrow.Table (Parquet)
        table = pa.Table.from_pandas(df)

        # Write parquet table.
        pq.write_table(table, out_parquet)
        
        # Reset all FP's
        out_parquet.seek(0)
        out.seek(0)

        return rows, out, out_parquet

    def extract_json(self, line):
        json_part = line[line.index('{'):]
        return json.loads(json_part)

    def has_valid_json(self, line):
        json_part = line[line.index('{'):]

        try:
            json.loads(json_part)
        except ValueError:
            return False

        return True

    def format_check(self, line):
        return self.has_valid_json(line)

    def get_uuid(self, data):
        raise NotImplementedError()

    def get_default_extension(self, sp):
        raise NotImplementedError()

    def json_to_csv(self, data):
        uuid = self.get_uuid(data)
        result = [data.get(header) for header in self.headers]
        return result, uuid

    def apply_df_types(self, df):
        int_fields = [k for k,v in self.header_fields if v == int]
        str_fields = [k for k,v in self.header_fields if v == str]
        bool_fields = [k for k,v in self.header_fields if v == bool]
        float_fields = [k for k,v in self.header_fields if v == float]

        df[float_fields] = df[float_fields].astype(float)
        df[int_fields] = df[int_fields].astype(int)
        df[bool_fields] = df[bool_fields].astype(bool)
        df[str_fields] = df[str_fields].astype(str)

        return df


