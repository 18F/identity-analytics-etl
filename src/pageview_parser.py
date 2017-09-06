import json
import csv
import io
import re
import hashlib

from .log_parser import Parser

class PageViewParser(Parser):
    table = 'pageviews'
    headers = ['method', 'path', 'format', 'controller', 'action',
               'status', 'duration', 'user_id', 'user_agent', 'ip',
               'host', 'uuid', 'timestamp']

    uuids = set()

    def stream_csv(self, in_io):
        rows = 0
        out = io.StringIO()
        writer = csv.writer(out, delimiter=',')
        writer.writerow(self.headers)

        for line in in_io.decode('utf-8').split('\n'):
            if ('{' not in line) or ('controller' not in line) or (not self.has_valid_json(line)):
                continue

            result, uuid = self.json_to_csv(self.extract_json(line))
            if uuid in self.uuids:
                continue

            self.uuids.add(uuid)
            writer.writerow(result)
            rows += 1

        out.seek(0)
        return rows, out

    def extract_json(self, line):
        return Parser.extract_json(self, line)

    def has_valid_json(self, line):
        return Parser.has_valid_json(self, line)

    def get_uuid(self, data):
        """
        Takes path, ip, timestamp, host, and duration and produces a sha256 hash
        to serve as a unique identifier that can be used to prevent duplicates
        """
        if data.get('uuid'):
            return data.get('uuid')
        else:
            return hashlib.sha256('|'.join([
                                            data['path'],
                                            data['ip'],
                                            data['timestamp'],
                                            data['host'],
                                            str(data['duration'])
                                          ]).encode('utf-8')
                                          ).hexdigest()

    def truncate_path(self, data):
        if data.get('path') is None:
            return None
        elif len(data.get('path')) < 1024:
            return data.get('path')
        elif '=' in data.get('path'):
            return data.get('path').split('=')[0]
        else:
            return data.get('path')[:1023]

    def json_to_csv(self, data):
        """
        Use .get to access the JSON as it is Null safe
        The RegEx replacement using \.\d+Z$ will convert a timestramp structured
        as 2017-04-10T17:45:22.754Z -> 2017-04-10 17:45:22
        """
        uuid = self.get_uuid(data)
        result = [
                  data.get('method'),
                  self.truncate_path(data),
                  data.get('format'),
                  data.get('controller'),
                  data.get('action'),
                  data.get('status'),
                  data.get('duration'),
                  data.get('user_id'),
                  data.get('user_agent'),
                  data.get('ip'),
                  data.get('host'),
                  uuid,
                  re.sub(r" \+\d+$", '', data.get('timestamp'))
                 ]

        return result, uuid
