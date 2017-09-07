import json


class Parser(object):

    def stream_csv(self, in_io):
        raise NotImplementedError()

    def extract_json(self, line):
        json_part = line[line.index('{'):]
        return json.loads(json_part)

    def has_valid_json(self, line):
        json_part = line[line.index('{'):]

        try:
            json.loads(json_part)
        except ValueError, e:
            return False

        return True

    def json_to_csv(self, data):
        raise NotImplementedError()
