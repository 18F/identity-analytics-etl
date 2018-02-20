import json
import csv
import re
import io

from .log_parser import Parser

class EmailParser(Parser):
    table = 'events_email'
    uuids = set()
    headers = ['id', 'name', 'domain_name', 'time']

    def stream_csv(self, in_io):
        return Parser.stream_csv(self, in_io)

    def extract_json(self, line):
        return Parser.extract_json(self, line)

    def has_valid_json(self, line):
        return Parser.has_valid_json(self, line)

    def get_uuid(self, data):
        return data.get('id')

    def format_check(self, line):
        if ('event_properties' not in line) or ('domain_name' not in line) or (not self.has_valid_json(line)):
            return True
        else:
            return False

    def json_to_csv(self, data):
        uuid = self.get_uuid(data)

        result = [
            data.get('id'),
            data.get('name'),
            data.get('properties').get('event_properties').get('domain_name'),
            re.sub(r"\.\d+Z$", '', data.get('time').replace('T', ' ')),
        ]

        return result, uuid