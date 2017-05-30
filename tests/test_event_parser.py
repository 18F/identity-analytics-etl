import unittest
import sys
import os
import json

from context import EventParser


class EventParserTestCases(unittest.TestCase):
    event_json = '{"id":"ff2d1183-3a82-42d6-8b08-19845ea8da3d","name":"Sign in page visited","properties":{"event_properties":{},"user_id":"anonymous-uuid","user_ip":"24.124.56.64","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","host":"idp.staging.login.gov"},"visit_id":"e6808a77-4c6f-4feb-bca6-fc88e5f67292","visitor_id":"76e2e090-0f78-4b77-b5a6-bd5c6c2e484e","time":"2017-04-10T17:45:22.754Z"}'
    in_io = open("{}/fixtures/test_event_log.txt".format(os.path.dirname(os.path.realpath(__file__))), 'rb').read()

    def test_stream_csv(self):
        parser = EventParser()
        rows, out = parser.stream_csv(self.in_io)
        self.assertEqual(rows, 1)

    def test_extract_json(self):
        parser = EventParser()
        res = parser.extract_json(self.event_json)
        self.assertEqual(res['id'], 'ff2d1183-3a82-42d6-8b08-19845ea8da3d')
        self.assertEqual(res['properties']['user_ip'], '24.124.56.64')
        self.assertEqual(res.keys(), json.loads(self.event_json).keys())

    def test_json_to_csv(self):
        parser = EventParser()
        data = json.loads(self.event_json)
        res = parser.json_to_csv(data)
        self.assertEqual(len(res), 20)
        self.assertEqual(res[8], '2017-04-10 17:45:22')
        self.assertFalse(res[-1])

if __name__ == '__main__':
    unittest.main()
