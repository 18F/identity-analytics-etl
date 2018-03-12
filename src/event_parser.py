import json
import csv
import re
import io

from .log_parser import Parser


class EventParser(Parser):
    table = 'events'
    header_fields = {
        'id': str,
        'name': str,
        'user_agent': str,
        'user_id': str,
        'user_ip': str,
        'host': str,
        'visit_id': str,
        'visitor_id': str,
        'time': str,
        'event_properties': str,
        'success': bool,
        'existing_user': bool,
        'otp_method': str,
        'context': str,
        'method': str,
        'authn_context': str,
        'service_provider': str,
        'loa3': bool,
        'active_profile': bool,
        'errors': str
    }

    uuids = set()
    service_provider_index = 6

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

    def get_default_extension(self, sp):
        res = [None] * 10
        res[self.service_provider_index] = sp
        return res

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
            extra = self.get_default_extension(sp)
            result.extend(extra)

        return result, uuid
