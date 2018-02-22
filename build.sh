cd build-analytics 
export MAIN_DIR=$(pwd)
apt-get update
apt-get install -y python-pip python3-pip python3-dev
cd /usr/local/bin
ln -s /usr/bin/python3 python
pip3 install --upgrade pip
cd $MAIN_DIR
apt-get install -y zip
apt-get install -y git
chmod u=rwx,go=r function.py
mkdir lambda_$1_deploy
cp -R src lambda_$1_deploy && cp function.py lambda_$1_deploy
pip3 install -Ur requirements.txt -t ./lambda_$1_deploy
cd lambda_$1_deploy
find * -type d -name tests -exec rm -rf {} \;
zip -r -q lambda_$1_deploy.zip .
cd ..
mv lambda_$1_deploy/lambda_$1_deploy.zip .
