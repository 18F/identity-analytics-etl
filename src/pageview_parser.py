import json
import csv
import io
import re
import parser

class PageViewParser(parser.Parser):
    table = 'pageviews'
    headers = ['method', 'path', 'format', 'controller', 'action',
               'status', 'duration', 'user_id', 'user_agent', 'ip',
               'host', 'uuid', 'timestamp']

    def stream_csv(self, in_io):
        rows = 0
        out = io.StringIO()
        writer = csv.writer(out, delimiter=',')
        writer.writerow(self.headers)

        for line in in_io.decode('utf-8').split('\n'):
            if ('{' not in line) or ('controller' not in line):
                continue

            writer.writerow(self.parse_json(self.extract_json(line)))
            rows += 1

        out.seek(0)
        return rows, out

    def extract_json(self, line):
        return parser.Parser.extract_json(self, line)

    def parse_json(self, data):
        # Use .get() because it is Null safe
        result = [
                  data.get('method'),
                  data.get('path'),
                  data.get('format'),
                  data.get('controller'),
                  data.get('action'),
                  data.get('status'),
                  data.get('duration'),
                  data.get('user_id'),
                  data.get('user_agent'),
                  data.get('ip'),
                  data.get('host'),
                  data.get('uuid'),
                  re.sub(r" \+\d+$", '', data.get('timestamp'))
                 ]

        return result
