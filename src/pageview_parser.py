import json
import csv
import io
import re

from .log_parser import Parser

class PageViewParser(Parser):
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

            writer.writerow(self.json_to_csv(self.extract_json(line)))
            rows += 1

        out.seek(0)
        return rows, out

    def extract_json(self, line):
        return Parser.extract_json(self, line)

    def json_to_csv(self, data):
        """
        Use .get to access the JSON as it is Null safe
        The RegEx replacement using \.\d+Z$ will convert a timestramp structured
        as 2017-04-10T17:45:22.754Z -> 2017-04-10 17:45:22
        """

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
