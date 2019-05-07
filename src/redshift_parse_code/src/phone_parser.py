import json
import csv
import re
import io

from .log_parser import BaseEventParser

class PhoneParser(BaseEventParser):
    table = 'events_phone'
    uuids = set()
    header_fields = {
        'id': str,
        'visit_id': str, 
        'visitor_id': str, 
        'area_code': str,
        'country_code': str,
        'time': str
    }

    AREA_CODE_PATTERN = '"area_code"'
    COUNTRY_CODE_PATTERN = '"country_code"'

    def get_uuid(self, data):
        return data.get('id')
    
    def is_valid_format(self, line, line_num):
        if (self.AREA_CODE_PATTERN in line) and (self.COUNTRY_CODE_PATTERN in line):
            return super(PhoneParser, self).is_valid_format(line, line_num)
        else:
            return False

    def json_to_csv(self, data):
        uuid = self.get_uuid(data)

        result = [
            data.get('id'),
            data.get('visit_id'),
            data.get('visitor_id'),
            data.get('properties').get('event_properties').get('area_code'),
            data.get('properties').get('event_properties').get('country_code'),
            re.sub(r"\.\d+Z$", '', data.get('time').replace('T', ' ')),
        ]

        return result, uuid
        