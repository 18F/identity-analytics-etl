import json
import csv
import io
import logging

# Try loading additional dependencies from tmp.

import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd


class Parser(object):
    header_fields = dict()
    json_cache = dict()  # key line number, value json data

    def stream_csv(self, in_io):
        parsed_rows = 0
        out = io.StringIO()
        out_parquet = io.BytesIO()
        header_rows = self.header_fields.keys()
        df_data = list()
        writer = csv.writer(out, delimiter=',')
        writer.writerow(header_rows)
        lines = in_io.decode('utf-8').split('\n')
        logging.info("got {} lines to parse".format(len(lines)))
        for line_num, line in enumerate(lines):
            if not self.is_valid_format(line, line_num):
                continue

            result, uuid = self.json_to_csv(self.extract_json(line, line_num))
            if uuid in self.uuids:
                continue

            self.uuids.add(uuid)
            writer.writerow(result)
            df_data.append(result)
            parsed_rows += 1
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

        total_rows = len(lines)
        return parsed_rows, total_rows, out, out_parquet

    def extract_json(self, line, line_num):
        if line_num in self.json_cache:
            return self.json_cache[line_num]
        else:
            try:
                time_part, logger_part, json_part = line.split(" ", 2)
            except ValueError:
                raise ValueError

            try:
                data = json.loads(json_part)
                self.json_cache[line_num] = data
                return data
            except ValueError:
                raise ValueError

    def has_valid_json(self, line, line_num):
        try:
            self.extract_json(line, line_num)
            return True
        except Exception as e:
            return False

    def is_valid_format(self, line, line_num):
        raise NotImplementedError

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


class BaseEventParser(Parser):
    JSON_PREFIX_PATTERN = '{"name":'
    ANALYTICS_EVENT_PATTERN = '"event_properties":'

    def is_valid_format(self, line, line_num):
        if (self.JSON_PREFIX_PATTERN in line) and (self.ANALYTICS_EVENT_PATTERN in line):
            return self.has_valid_json(line, line_num)
        else:
            return False
