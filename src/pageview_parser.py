import json
import csv
import io
import parser

class PageViewParser(parser.Parser):
    table = 'pageviews'
    headers = ['method', 'path', 'format', 'controller', 'action',
               'status', 'duration', 'user_id', 'user_agent', 'ip',
               'host', 'uuid', 'timestamp']

    def stream_csv(self, in_io):
        rows = 0
        out = io.StringIO()
        writer = csv.writer(out, delimiter=',')
        writer.writerow(self.headers)

        for line in in_io.decode('utf-8').split('\n'):
            if ('{' not in line) or ('controller' not in line):
                continue

            writer.writerow(self.parse_json(self.extract_json(line)))
            rows += 1

        return rows, out

    def extract_json(self, line):
        json_part = line[line.index('{'):]
        return json.loads(json_part)

    def parse_json(self, data):
        result = [
                  data['method'],
                  data['path'],
                  data['format'],
                  data['controller'],
                  data['action'],
                  data['status'],
                  data['duration'],
                  data['user_id'],
                  data['user_agent'],
                  data['ip'],
                  data['host'],
                  data['uuid'],
                  re.sub(r" \+\d+$/", '', data['timestamp'])
                 ]
        return result
