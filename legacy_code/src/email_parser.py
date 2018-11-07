import json
import csv
import re
import io

from .log_parser import Parser

class EmailParser(Parser):
    table = 'events_email'
    uuids = set()
    header_fields = {
        'id': str,
        'name': str, 
        'domain_name': str, 
        'time': str
    }

    def get_uuid(self, data):
        return data.get('id')

    def format_check(self, line, line_num):
        if ('event_properties' not in line) or ('domain_name' not in line) or (not self.has_valid_json(line, line_num)):
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
