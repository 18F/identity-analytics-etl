import json
import csv
import re
import parser

class EventParser(parser.Parser):
    table = 'events'
    headers = ['id', 'name', 'user_agent', 'user_id', 'user_ip',
               'host', 'visit_id', 'visitor_id', 'time', 'event_properties',
               'success', 'existing_user', 'otp_method', 'context',
               'method', 'authn_context', 'service_provider', 'loa3',
               'active_profile', 'errors']

    def stream_csv(self, in_io, out_io):
        rows = 0
        with open(out_io, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(self.headers)

            for line in in_io.decode('utf-8').split('\n'):
                if 'event_properties' not in line:
                    continue

                writer.writerow(self.parse_json(self.extract_json(line)))
                rows += 1

        return rows

    def extract_json(self, line):
        json_part = line[line.index('{'):]
        return json.loads(json_part)

    def parse_json(self, data):
        result = [
            data['id'],
            data['name'],
            data['properties']['user_agent'],
            data['properties']['user_id'],
            data['properties']['user_ip'],
            data['properties']['host'],
            data['visit_id'],
            data['visitor_id'],
            re.sub(r"/\.\d+Z$/", '', data['time'].replace('T', ' ')),
            json.dumps(data['properties']['event_properties'])
        ]

        if len(data['properties']['event_properties'].keys()) > 0:
            result.extend(
                [
                    data['properties']['event_properties']['success'],
                    data['properties']['event_properties']['existing_user'],
                    data['properties']['event_properties']['otp_method'],
                    data['properties']['event_properties']['context'],
                    data['properties']['event_properties']['method'],
                    data['properties']['event_properties']['authn_context'],
                    data['properties']['event_properties']['service_provider'],
                    data['properties']['event_properties']['loa3'],
                    data['properties']['event_properties']['active_profile'],
                    json.dumps(data['properties']['event_properties']['errors'])
                ]
            )
        else:
            result.extend(
                [None]*10
            )

        return result
