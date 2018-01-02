import json
import csv
import re
import io

from .log_parser import Parser

class DeviceParser(Parser):
    table = 'events_devices'
    uuids = set()
    headers = ['id', 'name', 'user_agent', 'browser_name', 'browser_version',
               'browser_platform_name', 'browser_platform_version',
               'browser_device_name', 'browser_device_type', 'browser_bot', 'time']

    def stream_csv(self, in_io):
        return Parser.stream_csv(self, in_io)

    def extract_json(self, line):
        return Parser.extract_json(self, line)

    def has_valid_json(self, line):
        return Parser.has_valid_json(self, line)

    def get_uuid(self, data):
        return data.get('id')

    def format_check(self, line):
        if ('event_properties' not in line) or ('browser' not in line) or (not self.has_valid_json(line)):
            return True
        else:
            return False

    def json_to_csv(self, data):
        uuid = self.get_uuid(data)

        result = [
            data.get('id'),
            data.get('name'),
            data.get('user_agent'),
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
