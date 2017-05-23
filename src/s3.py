import boto3

class S3:

    def __init__(self, source_bucket, dest_bucket):
        self.conn = boto3.resource('s3')
        self.source_bucket = self.conn.Bucket(source_bucket)
        self.dest_bucket = self.conn.Bucket(dest_bucket)

    def get_s3_logfiles(self):
        return [f.key for f in self.source_bucket.objects.all() if '.txt' in f.key]

    def get_logfile(self, filename):
        return self.source_bucket.Object(filename).get()['Body']

    def new_file(self, out, filename):
        self.dest_bucket.upload_fileobj(out, filename)
