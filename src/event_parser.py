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
            print(type(in_io))
            for line in in_io.decode('utf-8').split('\n'):
                print(line)
                if 'event_properties' not in line:
                    continue

                writer.writerow(self.parse_json(self.extract_json(line)))
                rows += 1

        return rows

    def extract_json(self, line):
        json_part = line[line.index('{'):-1]
        return json.loads(json_part)

    def parse_json(self, data):
        result = [
            json['id'],
            json['name'],
            json['properties']['user_agent'],
            json['properties']['user_id'],
            json['properties']['user_ip'],
            json['properites']['host'],
            json['visit_id'],
            json['visitor_id'],
            re.sub(r"/\.\d+Z$/", '', json['time'].replace('T', ' ')),
            json.dump(json['properties']['event_properties']),
            json['properties']['event_properties']['success'],
            json['properties']['event_properties']['existing_user'],
            json['properties']['event_properties']['otp_method'],
            json['properties']['event_properties']['context'],
            json['properties']['event_properties']['method'],
            json['properties']['event_properties']['authn_context'],
            json['properties']['event_properties']['service_provider'],
            json['properties']['event_properties']['loa3'],
            json['properties']['event_properties']['active_profile'],
            json.dump(json['properties']['event_properties']['errors'])
        ]

        return result
