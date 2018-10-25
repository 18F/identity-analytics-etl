import json
import csv
import re
import io

from .log_parser import Parser

class DeviceParser(Parser):
    table = 'events_devices'
    uuids = set()
    header_fields = {
        'id': str, 
        'name': str, 
        'user_agent': str, 
        'browser_name': str, 
        'browser_version': str, 
        'browser_platform_name': str, 
        'browser_platform_version': str, 
        'browser_device_name': str, 
        'browser_device_type': str, 
        'browser_bot': bool, 
        'time': str
    }

    def get_uuid(self, data):
        return data.get('id')

    def format_check(self, line, line_num):
        if ('event_properties' not in line) or ('browser' not in line) or (not self.has_valid_json(line, line_num)):
            return True
        else:
            return False

    def json_to_csv(self, data):
        uuid = self.get_uuid(data)

        result = [
            data.get('id'),
            data.get('name'),
            data.get('properties').get('user_agent'),
            data.get('properties').get('browser_name'),
            data.get('properties').get('browser_version'),
            data.get('properties').get('browser_platform_name'),
            data.get('properties').get('browser_platform_version'),
            data.get('properties').get('browser_device_name'),
            data.get('properties').get('browser_device_type'),
            data.get('properties').get('browser_bot'),
            re.sub(r"\.\d+Z$", '', data.get('time').replace('T', ' ')),
        ]

        return result, uuid
