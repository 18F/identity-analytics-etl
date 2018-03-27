import boto3
import io
import gzip
import pytz

from datetime import datetime, timedelta
from botocore.config import Config


class S3:

    def __init__(self, source_bucket, dest_bucket, dest_bucket_parquet, hot_bucket, encryption_key):
        self.conn = boto3.resource(
            's3',
            config=Config(signature_version='s3v4')
        )

        self.source_bucket = self.conn.Bucket(source_bucket)
        self.dest_bucket = self.conn.Bucket(dest_bucket)
        self.dest_bucket_parquet = self.conn.Bucket(dest_bucket_parquet)
        self.hot_bucket = self.conn.Bucket(hot_bucket)
        self.encryption_key = encryption_key
        self.key_check = lambda key: ('.txt' in key) and ('cloud' not in key)
        self.csv_check = lambda key: ('.csv' in key) and ('cloud' not in key)

    def get_n_s3_logfiles(self, n):
        get_last_modified = lambda x: int(x.last_modified.strftime('%s'))
        sorted_files = sorted(
                              [f for f in self.source_bucket.objects.filter()],
                              key=get_last_modified,
                              reverse=True
                              )

        return [f.key for f in sorted_files if self.key_check(f.key)][:n]

    def get_s3_logfiles_by_date_range(self, begin_date, end_date):
        get_last_modified = lambda x: int(x.last_modified.strftime('%s'))
        files = []

        for f in self.source_bucket.objects.filter():
            last_modified = f.last_modified.replace(tzinfo=pytz.UTC)
            if last_modified >= begin_date and last_modified <= end_date:
                files.append(f)

        sorted_files = sorted(
                              files,
                              key=get_last_modified,
                              reverse=True
                              )

        return [f.key for f in sorted_files if self.key_check(f.key)]

    def get_s3_logfiles_by_lookback(self, delta):
        time_ = datetime.utcnow().replace(tzinfo=pytz.utc)
        return self.get_s3_logfiles_by_date_range(time_ - delta, time_)

    def get_all_s3_logfiles(self):
        return [f.key for f in self.source_bucket.objects.all() if self.key_check(f.key)]

    def get_all_csv(self):
        get_last_modified = lambda x: int(x.last_modified.strftime('%s'))
        files = [f for f in self.hot_bucket.objects.all() if self.csv_check(f.key)]
        sorted_files = sorted(files, key=get_last_modified, reverse=False)
        return [f.key for f in sorted_files]

    def get_logfile(self, filename):
        return self.source_bucket.Object(filename).get()['Body']

    def new_file(self, out, filename):
        res = io.BytesIO(out.getvalue().encode('utf-8'))
        self.dest_bucket.upload_fileobj(
            res,
            filename,
            ExtraArgs={
                "SSEKMSKeyId": self.encryption_key,
                "ServerSideEncryption": 'aws:kms'
            }
        )

    def new_file_hot(self, out, filename):
        res = io.BytesIO(out.getvalue().encode('utf-8'))
        self.hot_bucket.upload_fileobj(
            res,
            filename,
            ExtraArgs={
                "SSEKMSKeyId": self.encryption_key,
                "ServerSideEncryption": 'aws:kms'
            }
        )

    def new_file_parquet(self, out, filename):
        self.dest_bucket_parquet.upload_fileobj(
            out,
            filename,
            ExtraArgs={
                "SSEKMSKeyId": self.encryption_key,
                "ServerSideEncryption": 'aws:kms'
            }
        )

    def create_dest_bucket_if_not_exists(self):
        if self.dest_bucket not in self.conn.buckets.all():
            self.dest_bucket = self.conn.create_bucket(Bucket=self.dest_bucket.name)

    def get_path(self, csv_name):
        return "s3://{}/{}".format(self.dest_bucket.name, csv_name)

    def download_file(self, filename):
        self.dest_bucket.download_file(filename, "/tmp/{}".format(filename))

    def delete_from_bucket(self, filename):
        self.hot_bucket.Object(filename).delete()
