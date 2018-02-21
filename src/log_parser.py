import json
import csv
import re
import io
import hashlib
import numpy as np

# Try loading additional dependencies from tmp.
import sys
sys.path.append('/tmp')
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


class Parser(object):
    headers = []

    def stream_csv(self, in_io):
        rows = 0
        out = io.StringIO()
        out_parquet = io.BytesIO()
        df = pd.DataFrame(columns=self.headers)
        writer = csv.writer(out, delimiter=',')
        writer.writerow(self.headers)

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
