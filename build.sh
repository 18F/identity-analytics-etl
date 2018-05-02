cd build-analytics
chmod u=rwx,go=r function.py
chmod u=rwx,go=r function_2.py
mkdir lambda_$1_deploy
mkdir lambda_$1_deploy_hot
cp -R src lambda_$1_deploy && cp function.py lambda_$1_deploy
cp -R src lambda_$1_deploy_hot && cp function_2.py lambda_$1_deploy_hot
pip3 install -Ur requirements.txt -t ./lambda_$1_deploy
pip3 install -Ur requirements.txt -t ./lambda_$1_deploy_hot
cd lambda_$1_deploy
find * -type d -name tests -exec rm -rf {} \;
zip -r -q lambda_$1_deploy.zip .
cd ..
mv lambda_$1_deploy/lambda_$1_deploy.zip .
cd lambda_$1_deploy_hot
find * -type d -name tests -exec rm -rf {} \;
zip -r -q lambda_$1_deploy_hot.zip .
cd ..
mv lambda_$1_deploy_hot/lambda_$1_deploy_hot.zip .
