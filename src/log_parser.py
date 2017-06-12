import json


class Parser(object):

    def stream_csv(self, in_io):
        raise NotImplementedError()

    def extract_json(self, line):
        json_part = line[line.index('{'):]
        return json.loads(json_part)

    def json_to_csv(self, data):
        raise NotImplementedError()
