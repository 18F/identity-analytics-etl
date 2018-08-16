help:
	@echo 'init - install pipenv and all project dependencies' 
	@echo 'test -  run all tests'
	@echo 'docker_start - start the docker daemon and pull the analytics docker image'

init: 
	pip install pipenv
	pipenv --python python3.6
	pipenv install 

docker_start: 
	docker pull 18fgsa/login-analytics 
	docker inspect analytics >/dev/null 2>&1 && echo "Docker container running" || docker run --name analytics -p 5431:5432 -v $(PWD):$(PWD) -d -t 18fgsa/login-analytics:latest 

docker_stop: 
	docker stop analytics && docker rm analytics

test: init docker_start
	bash test.sh

coverage: test
	pipenv run py.test --cov=src tests/

destroy_db:
	pipenv run python destroy_db.py

clean: init test destroy_db
	pipenv clean
	pipenv --rm

run: 
	pipenv run python upload_run.py

lambda_cleanup:
	rm -f lambda_$(TAG)_deploy.zip
	rm -rf lambda_$(TAG)_deploy/
	rm -f lambda_$(TAG)_deploy_hot.zip
	rm -rf lambda_$(TAG)_deploy_hot/

lambda_buckets:
	# TODO: Can We automate bucket logging here as well?
	aws s3 mb s3://login-gov-$(ENVIRONMENT)-$(ACCT_ID)-redshift-secrets
	aws s3 cp redshift_secrets.yml s3://login-gov-$(ENVIRONMENT)-$(ACCT_ID)-redshift-secrets/redshift_secrets.yml

lambda_build: lambda_cleanup
	echo "Running build."
	git tag -a $(TAG) -m "Deployed from Makefile"
	git push origin --tags
	docker exec --user root -it analytics bash -c "cd $(PWD) && bash build.sh $(TAG)"
	
lambda_release: clean lambda_build

lambda_deploy: lambda_release
	aws s3 cp lambda_$(TAG)_deploy.zip s3://tf-redshift-bucket-deployments/
	aws s3 cp lambda_$(TAG)_deploy_hot.zip s3://tf-redshift-bucket-deployments-hot/
	make lambda_cleanup
	make docker_stop
