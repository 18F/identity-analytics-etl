import json
import csv
import re
import io
import parser


class EventParser(parser.Parser):
    table = 'events'
    headers = ['id', 'name', 'user_agent', 'user_id', 'user_ip',
               'host', 'visit_id', 'visitor_id', 'time', 'event_properties',
               'success', 'existing_user', 'otp_method', 'context',
               'method', 'authn_context', 'service_provider', 'loa3',
               'active_profile', 'errors']

    def stream_csv(self, in_io):
        rows = 0
        out = io.StringIO()
        writer = csv.writer(out, delimiter=',')
        writer.writerow(self.headers)

        for line in in_io.decode('utf-8').split('\n'):
            if 'event_properties' not in line:
                continue

            writer.writerow(self.json_to_csv(self.extract_json(line)))
            rows += 1

        out.seek(0)
        return rows, out

    def extract_json(self, line):
        return parser.Parser.extract_json(self, line)

    def json_to_csv(self, data):
        """
        Use .get to access the JSON as it is Null safe
        The RegEx replacement using \.\d+Z$ will convert a timestramp structured
        as 2017-04-10T17:45:22.754Z -> 2017-04-10 17:45:22
        """

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
                    data['properties']['event_properties'].get('service_provider'),
                    data['properties']['event_properties'].get('loa3'),
                    data['properties']['event_properties'].get('active_profile'),
                    json.dumps(data['properties']['event_properties'].get('errors'))
                ]
            )
        else:
            result.extend(
                [None]*10
            )

        return result
