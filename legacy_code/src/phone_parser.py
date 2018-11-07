import json
import csv
import re
import io

from .log_parser import Parser

class PhoneParser(Parser):
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
    
    def get_uuid(self, data):
        return data.get('id')
    
    def format_check(self, line, line_num):
        if ('event_properties' not in line) or ('area_code' not in line) or ('country_code' not in line) or (not self.has_valid_json(line, line_num)):
            return True
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
        