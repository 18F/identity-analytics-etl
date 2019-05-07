# Current datapipeline flow of user-event driven data
This image displays how user event data travels from our application to various tools. This was generated with [Mermaid Chart](https://mermaidjs.github.io/) to generate [this](https://mermaidjs.github.io/mermaid-live-editor/#/view/eyJjb2RlIjoiZ3JhcGggVERcbkFbUHJvZHVjdGlvbiBBcHBsaWNhdGlvbl0gLS0-TltVc2VyIGRyaXZlbiBldmVudF1cbk4gLS4tPiBMW0dvb2dsZSBBbmFseXRpY3NdXG5OIC0tPiBCW0FXUyBDbG91ZFdhdGNoXVxuQiAtLi0-IE9bS2luZXNpc11cbk8tLi0-SlxuRCAtLT4gTVtSYXcgZGF0YSBzMyBidWNrZXRdXG5NIC0tPiBDW0xhbWJkYSBQYXJzZXJdXG5DIC0tPiBHW0hvdCBidWNrZXQgLUludGVybWVkaWF0ZSBTMyBidWNrZXRdXG5HIC0tPiBJW0xhbWRiYSAtUmVkU2hpZnQgTG9hZGVyXVxuSSAtLT4gSltSZWRTaGlmdF1cbkogLS0-IEhbQVdTIFF1aWNrU2l0ZV1cbkogLS4tPiBLW0JsYXplcl1cbk4gLS0-IERbTG9nc3Rhc2hdXG5EIC0tPiBFW0VsYXN0aVNlYXJjaF1cbkUgLS0-IEZbS2liYW5hXVxuXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9fQ)

![image](https://user-images.githubusercontent.com/5840989/52419390-f939a180-2abd-11e9-8689-416e6e6a7afa.png)

```
graph TD
A[Production Application] -->N[User driven event]
N -.-> L[Google Analytics]
N --> B[AWS CloudWatch]
B -.-> O[Kinesis]
O-.->J
D --> M[Raw data s3 bucket]
M --> C[Lambda Parser]
C --> G[Hot bucket -Intermediate S3 bucket]
G --> I[Lamdba -RedShift Loader]
I --> J[RedShift]
J --> H[AWS QuickSite]
J -.-> K[Blazer]
N --> D[Logstash]
D --> E[ElastiSearch]
E --> F[Kibana]

```
