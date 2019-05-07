#!/bin/bash
chmod u=rwx,go=r function.py
chmod u=rwx,go=r function_2.py
mkdir deps
mkdir lambda_$1_deploy
mkdir lambda_$1_deploy_hot
cp -R src lambda_$1_deploy && cp function.py lambda_$1_deploy
cp -R src lambda_$1_deploy_hot && cp function_2.py lambda_$1_deploy_hot
pip3 install -Ur requirements.txt -t ./deps
cd deps
find * -type d -name tests -exec rm -rf {} \;
cd ..
cp -r deps/. lambda_$1_deploy_hot
cp -r deps/. lambda_$1_deploy
cd lambda_$1_deploy
zip -r -q lambda_$1_deploy.zip .
cd ..
mv lambda_$1_deploy/lambda_$1_deploy.zip .
cd lambda_$1_deploy_hot
zip -r -q lambda_$1_deploy_hot.zip .
cd ..
mv lambda_$1_deploy_hot/lambda_$1_deploy_hot.zip .
rm -rf deps
