import json
import csv
import io
import re
import hashlib

from .log_parser import Parser


class PageViewParser(Parser):
    table = 'pageviews'
    header_fields = {
        'method': str,
        'path': str,
        'format': str,
        'controller': str,
        'action': str,
        'status': int,
        'duration': float,
        'user_id': str,
        'user_agent': str,
        'ip': str,
        'host': str,
        'uuid': str,
        'timestamp': str
    }

    uuids = set()

    JSON_PREFIX_PATTERN = '"method":'
    PATH_PATTERN = '"path":'
    CONTROLLER_PATTERN = '"controller":'

    def is_valid_format(self, line, line_num):
        if (self.JSON_PREFIX_PATTERN in line) and (self.PATH_PATTERN in line) and (self.CONTROLLER_PATTERN in line):
            return self.has_valid_json(line, line_num)
        else:
            return False

    def get_uuid(self, data):
        """
        Takes path, ip, timestamp, host, and duration and produces a sha256 hash
        to serve as a unique identifier that can be used to prevent duplicates
        """
        if data.get('uuid'):
            return data.get('uuid')
        else:
            return hashlib.sha256(
                '|'.join([
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
        The RegEx replacement using \.\d+Z$ will convert a timestramp
        structured as 2017-04-10T17:45:22.754Z -> 2017-04-10 17:45:22
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
