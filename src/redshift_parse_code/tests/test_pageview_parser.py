import unittest
import sys
import os
import json

from context import PageViewParser
from io import BytesIO


class PageViewParserTestCases(unittest.TestCase):
    pageview_json = '2017-04-10T17:45:22.600Z idp {"method":"GET","path":"/?issuer=&timeout=true","format":"html","controller":"Users::SessionsController","action":"new","status":302,"duration":4.84,"location":"https://idp.staging.login.gov/?issuer=","user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000","uuid":"58d753fe-4542-437f-a812-1f0f146cb4ec"}'
    pageview_json_no_id = '2017-04-10T17:45:22.600Z idp {"method":"GET","path":"/?issuer=&timeout=true","format":"html","controller":"Users::SessionsController","action":"new","status":302,"duration":4.84,"location":"https://idp.staging.login.gov/?issuer=","user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000"}'
    test_pageview_log_txt = BytesIO(b"""
     2017-04-10T17:45:22.600Z idp 172.16.33.245 - - [10/Apr/2017:17:45:21 +0000] "GET / HTTP/1.1" 401 188 "-" "ELB-HealthChecker/2.0"
     2017-04-10T17:45:23.600Z idp 172.16.33.245 - 18f [10/Apr/2017:17:45:22 +0000] "GET /?issuer=&timeout=true HTTP/1.1" 302 115 "https://idp.staging.login.gov/?issuer=" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
     2017-04-10T17:45:23.600Z idp 172.16.33.245 - 18f [10/Apr/2017:17:45:22 +0000] "GET /?issuer= HTTP/1.1" 200 9087 "https://idp.staging.login.gov/?issuer=" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
     2017-04-10T17:45:25.438Z idp {"method":"GET","path":"/?issuer=&timeout=true","format":"html","controller":"Users::SessionsController","action":"new","status":302,"duration":4.84,"location":"https://idp.staging.login.gov/?issuer=","user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000","uuid":"58d753fe-4542-437f-a812-1f0f146cb4ec"}
     2017-04-10T17:45:25.438Z idp {"method":"GET","path":"/?issuer=","format":"html","controller":"Users::SessionsController","action":"new","status":200,"duration":13.59,"user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000","uuid":"a7617fe8-87b7-4f67-8e50-ebc90a2d3fbe"}
     2017-03-31T19:38:48.835Z elk type=PATH msg=audit(1490935667.633:579960): item=0 name="/usr/src/linux-headers-3.13.0-107/include/dt-bindings/interrupt-controller/" inode=22764 dev=ca:01 mode=040755 ouid=0 ogid=0 rdev=00:00 nametype=PARENT
     2017-03-31T19:38:48.835Z elk type=PATH msg=audit(1490935667.633:579960): item=1 name="/usr/src/linux-headers-3.13.0-107/include/dt-bindings/interrupt-controller/arm-gic.h" inode=23233 dev=ca:01 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=DELETE
     2017-04-06T06:57:09.449Z jenkins f++++++++++++++++: /var/chef/cache/identity-idp/spec/support/controller_helper.rb

    """)
    in_io = test_pageview_log_txt.read()

    def test_stream_csv(self):
        parser = PageViewParser()
        parsed_rows, total_rows, out, out_parquet = parser.stream_csv(self.in_io)
        self.assertEqual(parsed_rows, 2)
        self.assertTrue(len(out_parquet.read()) > 0)

    def test_extract_json(self):
        parser = PageViewParser()
        data = parser.extract_json(self.pageview_json, line_num=1)
        self.assertEqual(data['method'], 'GET')
        self.assertEqual(data['uuid'], '58d753fe-4542-437f-a812-1f0f146cb4ec')

    def test_json_to_csv(self):
        parser = PageViewParser()
        data = parser.extract_json(self.pageview_json, line_num=1)
        res = parser.json_to_csv(data)[0]
        self.assertEqual(len(res), 13)
        self.assertEqual(res[12], '2017-04-10 17:45:22')

    def test_get_uuid(self):
        parser = PageViewParser()
        data = parser.extract_json(self.pageview_json_no_id, line_num=2)
        res = parser.get_uuid(data)
        self.assertEqual(res, 'da76b7beeff3142b8343f4e4281ded230f9c1c9c0092c4278769f1ec16e70423')

    def test_truncate_path(self):
        parser = PageViewParser()
        data = parser.extract_json(self.pageview_json, line_num=1)
        res = parser.truncate_path(data)
        self.assertEqual(res, data.get('path'))


if __name__ == '__main__':
    unittest.main()
