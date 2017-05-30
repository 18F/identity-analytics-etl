import unittest
import sys
import os
import json

from context import PageViewParser


class PageViewParserTestCases(unittest.TestCase):
    pageview_json = '{"method":"GET","path":"/?issuer=&timeout=true","format":"html","controller":"Users::SessionsController","action":"new","status":302,"duration":4.84,"location":"https://idp.staging.login.gov/?issuer=","user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000","uuid":"58d753fe-4542-437f-a812-1f0f146cb4ec"}'
    in_io = open("{}/tests/test_pageview_log.txt".format(os.getcwd()), 'rb').read()

    def test_stream_csv(self):
        parser = PageViewParser()
        rows, out = parser.stream_csv(self.in_io)
        self.assertEqual(rows, 2)

    def test_extract_json(self):
        parser = PageViewParser()
        res = parser.extract_json(self.pageview_json)
        self.assertEqual(res['method'], 'GET')
        self.assertEqual(res['uuid'], '58d753fe-4542-437f-a812-1f0f146cb4ec')
        self.assertEqual(res.keys(), json.loads(self.pageview_json).keys())

    def test_parse_json(self):
        parser = PageViewParser()
        data = json.loads(self.pageview_json)
        res = parser.parse_json(data)
        self.assertEqual(len(res), 13)
        self.assertEqual(res[12], '2017-04-10 17:45:22')


if __name__ == '__main__':
    unittest.main()
