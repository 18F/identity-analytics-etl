import src
import os

if __name__ == '__main__':
    if 'env' in os.environ.keys():
        bucket = "login-gov-{}-analytics".format(os.environ['env'])
    else:
        bucket = 'tf-redshift-bucket-dev-analytics'

    uploader = src.Uploader('login-gov-prod-logs', bucket)
    uploader.run()
