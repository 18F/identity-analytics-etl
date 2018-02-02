cd build-analytics \
&& apt-get update \
&& apt-get install python-pip \
&& apt-get install zip \
&& apt-get install git \
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