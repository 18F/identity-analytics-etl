import boto3
import io

class S3:

    def __init__(self, source_bucket, dest_bucket):
        self.conn = boto3.resource('s3')
        self.source_bucket = self.conn.Bucket(source_bucket)
        self.dest_bucket = self.conn.Bucket(dest_bucket)

    def get_s3_logfiles(self):
        get_last_modified = lambda x: int(x.last_modified.strftime('%s'))
        sorted_files = sorted(
                              [f for f in self.source_bucket.objects.filter()],
                              key=get_last_modified,
                              reverse=True
                              )

        return [f.key for f in sorted_files if '.txt' in f.key][:9]

    def get_all_s3_logfiles(self):
        return [f.key for f in self.source_bucket.objects.all() if '.txt' in f.key]

    def get_logfile(self, filename):
        return self.source_bucket.Object(filename).get()['Body']

    def new_file(self, out, filename):
        res = io.BytesIO(out.getvalue().encode('utf-8'))
        self.dest_bucket.upload_fileobj(res, filename)

    def create_dest_bucket_if_not_exists(self):
        if self.dest_bucket not in self.conn.buckets.all():
            self.dest_bucket = self.conn.create_bucket(Bucket=self.dest_bucket.name)

    def get_path(self, csv_name):
        return "s3://{}/{}".format(self.dest_bucket.name, csv_name)

    def download_file(self, filename):
        self.dest_bucket.download_file(filename, "/tmp/{}".format(filename))
