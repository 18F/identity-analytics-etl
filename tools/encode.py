import base64
import StringIO
import gzip
import argparse
import sys

data=''
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="String to zip and encode Base64")
    args = parser.parse_args()
    data = args.data
except:
    e = sys.exc_info()[0]
    print (e)

out = StringIO.StringIO()
with gzip.GzipFile(fileobj=out, mode='w') as f:
    f.write(data)
print(base64.b64encode(out.getvalue()))
