import json
import csv

class PageViewParser:
    table = 'pageviews'
    headers = ['method', 'path', 'format', 'controller', 'action',
               'status', 'duration', 'user_id', 'user_agent', 'ip',
               'host', 'uuid', 'timestamp']

    def stream_csv(self, in_io, out_io):
        rows = 0

        with open(out_io, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(self.headers)

            with open(in_io, 'rb') as f:
                for line in f:
                    if ('{' not in line) or ('controller' not in line):
                        continue

                    writer.writerow(self.parse_json(self.extract_json(line)))
                    rows += 1

        return rows

    def extract_json(line):
        json_part = line[line.index('{'):-1]
        return json.loads(json_part)

    def parse_json(data):
        result = [
                  json['method'],
                  json['path'],
                  json['format'],
                  json['controller'],
                  json['action'],
                  json['status'],
                  json['duration'],
                  json['user_id'],
                  json['user_agent'],
                  json['ip'],
                  json['host'],
                  json['uuid'],
                  re.sub(r" \+\d+$/", '', json['timestamp'])
                 ]
        return result
