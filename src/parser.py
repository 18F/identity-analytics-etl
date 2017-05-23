class Parser(object):

    def stream_csv(self, in_io):
        raise NotImplementedError()

    def extract_json(self, line):
        raise NotImplementedError()

    def parse_json(self, data):
        raise NotImplementedError()
