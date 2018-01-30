import unittest
import sys
import os
import json

from context import PageViewParser


class PageViewParserTestCases(unittest.TestCase):
    pageview_json = '{"method":"GET","path":"/?issuer=&timeout=true","format":"html","controller":"Users::SessionsController","action":"new","status":302,"duration":4.84,"location":"https://idp.staging.login.gov/?issuer=","user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000","uuid":"58d753fe-4542-437f-a812-1f0f146cb4ec"}'
    pageview_json_no_id = '{"method":"GET","path":"/?issuer=&timeout=true","format":"html","controller":"Users::SessionsController","action":"new","status":302,"duration":4.84,"location":"https://idp.staging.login.gov/?issuer=","user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000"}'
    in_io = open("{}/fixtures/test_pageview_log.txt".format(os.path.dirname(os.path.realpath(__file__))), 'rb').read()

    def test_stream_csv(self):
        parser = PageViewParser()
        rows, out, out_parquet = parser.stream_csv(self.in_io)
        self.assertEqual(rows, 2)
        self.assertTrue(len(out_parquet.read()) > 0)

    def test_extract_json(self):
        parser = PageViewParser()
        res = parser.extract_json(self.pageview_json)
        self.assertEqual(res['method'], 'GET')
        self.assertEqual(res['uuid'], '58d753fe-4542-437f-a812-1f0f146cb4ec')
        self.assertEqual(res.keys(), json.loads(self.pageview_json).keys())

    def test_json_to_csv(self):
        parser = PageViewParser()
        data = json.loads(self.pageview_json)
        res = parser.json_to_csv(data)[0]
        self.assertEqual(len(res), 13)
        self.assertEqual(res[12], '2017-04-10 17:45:22')

    def test_get_uuid(self):
        parser = PageViewParser()
        data = json.loads(self.pageview_json_no_id)
        res = parser.get_uuid(data)
        self.assertEqual(res, 'da76b7beeff3142b8343f4e4281ded230f9c1c9c0092c4278769f1ec16e70423')

    def test_truncate_path(self):
        parser = PageViewParser()
        data = json.loads(self.pageview_json)
        res = parser.truncate_path(data)
        self.assertEqual(res, data.get('path'))


if __name__ == '__main__':
    unittest.main()
