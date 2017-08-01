import io
import os


class FakeS3:

    def __init__(self, source_bucket, dest_bucket):
        self.source_bucket = source_bucket
        self.dest_bucket = dest_bucket
        self.content = {'c.txt': "{}/fixtures/test_event_log.txt".format(os.path.dirname(os.path.realpath(__file__))),
                        'd.txt': "{}/fixtures/test_pageview_log.txt".format(os.path.dirname(os.path.realpath(__file__)))}
        self.output = {}

    def get_s3_logfiles(self):
        return [f for f in self.content.keys() if '.txt' in f]

    def get_n_s3_logfiles(self, n):
        return self.get_s3_logfiles()

    def get_s3_logfiles_by_lookback(self, delta):
        return self.get_s3_logfiles()

    def get_logfile(self, filename):
        return open(self.content.get(filename), 'rb')

    def new_file(self, out, filename):
        self.output[filename] = out.getvalue()
        with open(self.get_path(filename), 'w') as f:
            f.write(out.getvalue())

    def create_dest_bucket_if_not_exists(self):
        pass

    def get_path(self, csv_name):
        return "{}/fixtures/{}".format(os.path.dirname(os.path.realpath(__file__)), csv_name)
