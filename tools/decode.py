import base64
import StringIO
import gzip
import json
import argparse
import sys

data=''
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="Base64 string to unzip")
    args = parser.parse_args()
    data = args.data
except:
    e = sys.exc_info()[0]
    print (e)

data = base64.b64decode(data)
striodata = StringIO.StringIO(data)
with gzip.GzipFile(fileobj=striodata, mode='r') as f:
    output = json.loads(f.read())

print (json.dumps(output))
