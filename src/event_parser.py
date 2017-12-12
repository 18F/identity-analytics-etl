import json
import csv
import re
import io

from .log_parser import Parser


class EventParser(Parser):
    table = 'events'
    headers = ['id', 'name', 'user_agent', 'user_id', 'user_ip',
               'host', 'visit_id', 'visitor_id', 'time', 'event_properties',
               'success', 'existing_user', 'otp_method', 'context',
               'method', 'authn_context', 'service_provider', 'loa3',
               'active_profile', 'errors']
    uuids = set()

    def stream_csv(self, in_io):
        return Parser.stream_csv(self, in_io)

    def extract_json(self, line):
        return Parser.extract_json(self, line)

    def has_valid_json(self, line):
        return Parser.has_valid_json(self, line)

    def format_check(self, line):
        if 'event_properties' not in line or not self.has_valid_json(line):
            return True
        else:
            return False

    def get_uuid(self, data):
        return data.get('id')

    def json_to_csv(self, data):
        """
        Use .get to access the JSON as it is Null safe
        The RegEx replacement using \.\d+Z$ will convert a timestramp
        structured as 2017-04-10T17:45:22.754Z -> 2017-04-10 17:45:22
        """

        uuid = self.get_uuid(data)
        sp = data.get('properties').get('service_provider')

        result = [
            data.get('id'),
            data.get('name'),
            data.get('properties').get('user_agent'),
            data.get('properties').get('user_id'),
            data.get('properties').get('user_ip'),
            data.get('properties').get('host'),
            data.get('visit_id'),
            data.get('visitor_id'),
            re.sub(r"\.\d+Z$", '', data.get('time').replace('T', ' ')),
            json.dumps(data.get('properties').get('event_properties'))
        ]

        if len(data.get('properties').get('event_properties').keys()) > 0:
            result.extend(
                [
                    data['properties']['event_properties'].get('success'),
                    data['properties']['event_properties'].get('existing_user'),
                    data['properties']['event_properties'].get('otp_method'),
                    data['properties']['event_properties'].get('context'),
                    data['properties']['event_properties'].get('method'),
                    data['properties']['event_properties'].get('authn_context'),
                    sp,
                    data['properties']['event_properties'].get('loa3'),
                    data['properties']['event_properties'].get('active_profile'),
                    json.dumps(data['properties']['event_properties'].get('errors'))
                ]
            )
        else:
            extra = [None] * 6 + [sp] + [None] * 3
            result.extend(extra)

        return result, uuid
