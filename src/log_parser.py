import json
import csv
import io
import logging

# Try loading additional dependencies from tmp.

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

class Parser(object):
    header_fields = {}

    def stream_csv(self, in_io):
        rows = 0
        out = io.StringIO()
        out_parquet = io.BytesIO()
        header_rows = self.header_fields.keys()
        df_data = list()
        writer = csv.writer(out, delimiter=',')
        writer.writerow(header_rows)

        lines = in_io.decode('utf-8').split('\n')
        logging.info("got {} lines to parse".format(len(lines)))
        for line in lines:
            if self.format_check(line):
                continue

            result, uuid = self.json_to_csv(self.extract_json(line))
            if uuid in self.uuids:
                continue

            self.uuids.add(uuid)
            writer.writerow(result)
            df_data.append(result)
            rows += 1
        df = pd.DataFrame(df_data, columns=header_rows)

        # Pyarrow tries to infer types by default.
        # Explicitly set the types to prevent mis-typing.
        df = self.apply_df_types(df)

        # Convert pandas.DataFrame -> pyarrow.Table (Parquet)
        table = pa.Table.from_pandas(df)

        # Write parquet table.
        pq.write_table(table, out_parquet, compression='snappy')

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
        result = [data.get(header) for header in self.header_fields.keys()]
        return result, uuid

    def apply_df_types(self, df):
        for k, v in self.header_fields.items():
            df[k] = df[k].astype(v)
        return df


