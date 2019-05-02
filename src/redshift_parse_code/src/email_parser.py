import json
import csv
import re
import io

from .log_parser import BaseEventParser

class EmailParser(BaseEventParser):
    table = 'events_email'
    uuids = set()
    header_fields = {
        'id': str,
        'name': str, 
        'domain_name': str, 
        'time': str
    }

    DOMAIN_PATTERN = '"domain_name"'

    def get_uuid(self, data):
        return data.get('id')

    def is_valid_format(self, line, line_num):
        if  self.DOMAIN_PATTERN in line:
            return super(EmailParser, self).is_valid_format(line, line_num)
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
