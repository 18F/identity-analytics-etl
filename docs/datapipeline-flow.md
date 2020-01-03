# Current datapipeline flow of user-event driven data
This image displays how user event data travels from our application to various tools. This was generated with [Mermaid Chart](https://mermaidjs.github.io/) to generate [this](https://mermaidjs.github.io/mermaid-live-editor/#/view/eyJjb2RlIjoiZ3JhcGggVERcbkFbUHJvZHVjdGlvbiBBcHBsaWNhdGlvbl0gLS0-TltVc2VyIGRyaXZlbiBldmVudF1cbk4gLS0-IExbR29vZ2xlIEFuYWx5dGljc11cbk4gLS0-UFtQcm9kdWN0aW9uIGRhdGFiYXNlXVxuUCAtLT5RW1JlYWQgcmVwbGljYSBkYXRhYmFzZV1cblEtLT5SW1MzIGJ1Y2tldHNdXG5SLS0-U1tKc29uIGRvd25sb2Fkc11cbk4gLS0-IEJbQVdTIENsb3VkV2F0Y2ggLSBldmVudHMubG9nXVxuQiAtLi0-IE9bS2luZXNpc11cbk8tLi0-SlxuQiAtLT4gTVtSYXcgZGF0YSBzMyBidWNrZXRdXG5CIC0tPiBDW0xhbWJkYSBQYXJzZXJdXG5DIC0tPiBHW0hvdCBidWNrZXQgLUludGVybWVkaWF0ZSBTMyBidWNrZXRdXG5HIC0tPiBJW0xhbWRiYSAtUmVkU2hpZnQgTG9hZGVyXVxuSSAtLT4gSltSZWRTaGlmdF1cbkogLS0-IEhbQVdTIFF1aWNrU2l0ZV1cbkIgLS0-IERbTG9nc3Rhc2hdXG5EIC0tPiBFW0VsYXN0aVNlYXJjaF1cbkUgLS0-IEZbS2liYW5hXVxuQi0tPlRbQ2xvdWQgd2F0Y2ggZGFzaGJvYXJkICYgaW5zaWdodHNdXG4iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9fQ)

![image](https://user-images.githubusercontent.com/5840989/71732020-357f9a00-2e14-11ea-9019-95556012f6d7.png)

```
graph TD
A[Production Application] -->N[User driven event]
N --> L[Google Analytics]
N -->P[Production database]
N --> B[AWS CloudWatch - events.log]
P -->Q[Read replica database]
Q-->R[S3 buckets]
R-->S[Json downloads]
B -.-> O[Kinesis]
O-.->J
B --> M[Raw data s3 bucket]
B --> C[Lambda Parser]
C --> G[Hot bucket -Intermediate S3 bucket]
G --> I[Lamdba -RedShift Loader]
I --> J[RedShift]
J --> H[AWS QuickSite]
B --> D[Logstash]
N --> |FileBeats| D 
D --> E[ElastiSearch]
E --> F[Kibana]
B-->T[Cloud watch dashboard & insights]

```
