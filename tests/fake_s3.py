import io
import os


class FakeS3:

    TEST_EVENT_LOG_TXT = io.BytesIO(b"""
     2017-04-10T17:45:24.621Z idp 172.16.33.245 - - [10/Apr/2017:17:45:21 +0000] "GET / HTTP/1.1" 401 188 "-" "ELB-HealthChecker/2.0"
     2017-04-10T17:45:24.621Z idp 172.16.33.245 - - [10/Apr/2017:17:45:23 +0000] "GET /manifest.json HTTP/1.1" 304 0 "https://idp.staging.login.gov/?issuer=" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
     2017-04-10T17:45:28.382Z idp Apr 10 17:45:22 idp ossec: Alert Level: 5; Rule: 31101 - Web server 400 error code.; Location: idp->/opt/nginx/logs/access.log; srcip: 172.16.33.245; 172.16.33.245 - - [10/Apr/2017:17:45:21 +0000] "GET / HTTP/1.1" 401 188 "-" "ELB-HealthChecker/2.0"
     2017-04-10T17:45:29.473Z idp {"id":"ff2d1183-3a82-42d6-8b08-19845ea8da3d","name":"Sign in page visited","properties":{"event_properties":{},"user_id":"anonymous-uuid","user_ip":"24.124.56.64","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","host":"idp.staging.login.gov"},"visit_id":"e6808a77-4c6f-4feb-bca6-fc88e5f67292","visitor_id":"76e2e090-0f78-4b77-b5a6-bd5c6c2e484e","time":"2017-04-10T17:45:22.754Z"}
     2017-04-10T17:45:29.022Z idp Apr 10 17:45:21 idp ossec: Alert Level: 5; Rule: 31101 - Web server 400 error code.; Location: idp->/opt/nginx/logs/access.log; srcip: 172.16.33.245; 172.16.33.245 - - [10/Apr/2017:17:45:21 +0000] "GET / HTTP/1.1" 401 188 "-" "ELB-HealthChecker/2.0"
     2017-04-10T17:45:43.383Z idp Apr 10 17:45:40 idp ossec: Alert Level: 5; Rule: 31101 - Web server 400 error code.; Location: idp->/opt/nginx/logs/access.log; srcip: 172.16.33.233; 172.16.33.233 - - [10/Apr/2017:17:45:39 +0000] "GET / HTTP/1.1" 401 188 "-" "ELB-HealthChecker/2.0"
     2017-04-10T17:45:44.023Z idp Apr 10 17:45:41 idp ossec: Alert Level: 5; Rule: 31101 - Web server 400 error code.; Location: idp->/opt/nginx/logs/access.log; srcip: 172.16.33.233; 172.16.33.233 - - [10/Apr/2017:17:45:39 +0000] "GET / HTTP/1.1" 401 188 "-" "ELB-HealthChecker/2.0"
    """)

    TEST_PAGEVIEW_LOG_TXT = io.BytesIO(b"""
    2017-04-10T17:45:22.600Z idp 172.16.33.245 - - [10/Apr/2017:17:45:21 +0000] "GET / HTTP/1.1" 401 188 "-" "ELB-HealthChecker/2.0"
    2017-04-10T17:45:23.600Z idp 172.16.33.245 - 18f [10/Apr/2017:17:45:22 +0000] "GET /?issuer=&timeout=true HTTP/1.1" 302 115 "https://idp.staging.login.gov/?issuer=" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    2017-04-10T17:45:23.600Z idp 172.16.33.245 - 18f [10/Apr/2017:17:45:22 +0000] "GET /?issuer= HTTP/1.1" 200 9087 "https://idp.staging.login.gov/?issuer=" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    2017-04-10T17:45:25.438Z idp {"method":"GET","path":"/?issuer=&timeout=true","format":"html","controller":"Users::SessionsController","action":"new","status":302,"duration":4.84,"location":"https://idp.staging.login.gov/?issuer=","user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000","uuid":"58d753fe-4542-437f-a812-1f0f146cb4ec"}
    2017-04-10T17:45:25.438Z idp {"method":"GET","path":"/?issuer=","format":"html","controller":"Users::SessionsController","action":"new","status":200,"duration":13.59,"user_id":"anonymous-uuid","user_agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36","ip":"24.124.56.64","host":"idp.staging.login.gov","timestamp":"2017-04-10 17:45:22 +0000","uuid":"a7617fe8-87b7-4f67-8e50-ebc90a2d3fbe"}
    2017-03-31T19:38:48.835Z elk type=PATH msg=audit(1490935667.633:579960): item=0 name="/usr/src/linux-headers-3.13.0-107/include/dt-bindings/interrupt-controller/" inode=22764 dev=ca:01 mode=040755 ouid=0 ogid=0 rdev=00:00 nametype=PARENT
    2017-03-31T19:38:48.835Z elk type=PATH msg=audit(1490935667.633:579960): item=1 name="/usr/src/linux-headers-3.13.0-107/include/dt-bindings/interrupt-controller/arm-gic.h" inode=23233 dev=ca:01 mode=0100644 ouid=0 ogid=0 rdev=00:00 nametype=DELETE
    2017-04-06T06:57:09.449Z jenkins f++++++++++++++++: /var/chef/cache/identity-idp/spec/support/controller_helper.rb
    """)
    def __init__(self, source_bucket, dest_bucket):
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.content = {'c.txt': "TEST_EVENT_LOG_TXT",
                        'd.txt': "TEST_PAGE_VIEW_LOG_TXT"}
        self.output = {}

    def get_s3_logfiles(self):
        return [f for f in self.content.keys() if '_TXT' in f]

    def get_n_s3_logfiles(self, n):
        return self.get_s3_logfiles()

    def get_s3_logfiles_by_lookback(self, delta):
        return self.get_s3_logfiles()

    def get_logfile(self, filename):
        return self.content.get(filename).read()

    def new_file(self, filename):
        self.output[filename] = self.content.get(filename).getvalue()

    def create_dest_bucket_if_not_exists(self):
        pass

    def get_path(self, csv_name):
        return "/fixtures/{}".format(csv_name)
