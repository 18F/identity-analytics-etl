import src
import os

if __name__ == '__main__':
    os.environ['S3_USE_SIGV4'] = 'True'
    if 'env' in os.environ.keys():
        bucket = "login-gov-{}-analytics".format(os.environ['env'])
    else:
        bucket = 'login-gov-prod-analytics'

    uploader = src.Uploader('login-gov-prod-logs', bucket)
    uploader.run()
