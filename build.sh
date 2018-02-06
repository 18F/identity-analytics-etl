cd build-analytics \
&& export MAIN_DIR=$(pwd) \
&& apt-get update \
&& apt-get install -y python-pip \
&& apt-get install -y python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip \
&& cd $MAIN_DIR \
&& apt-get install -y zip \
&& apt-get install -y git \
&& chmod u=rwx,go=r function.py \
&& mkdir lambda_$1_deploy \
&& cp -R src lambda_$1_deploy && cp function.py lambda_$1_deploy \
&& pip install -Ur requirements.txt -t ./lambda_$1_deploy \
&& git clone https://github.com/jkehler/awslambda-psycopg2.git \
&& rm -rf lambda_$1_deploy/psycopg2 \
&& mv awslambda-psycopg2/psycopg2-3.6 lambda_$1_deploy/psycopg2 \
&& rm -rf awslambda-psycopg2 \
&& cd lambda_$1_deploy \
&& zip -r -q lambda_$1_deploy.zip . \
&& cd .. \
&& mv lambda_$1_deploy/lambda_$1_deploy.zip .