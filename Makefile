venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

test: venv
	venv/bin/python tests/test.py

destroy_db:
	venv/bin/python destroy_db.py

clean: venv destroy_db test
	rm -rf venv

run: venv
	venv/bin/python upload_run.py

lambda_cleanup:
	rm -f lambda_$(TAG)_deploy.zip
	rm -rf lambda_$(TAG)_deploy/

lambda_buckets:
	# TODO: Can We automate bucket logging here as well?
	aws s3 mb s3://login-gov-$(ENVIRONMENT)-redshift-secrets
	aws s3 cp redshift_secrets.yml s3://login-gov-$(ENVIRONMENT)-redshift-secrets/redshift_secrets.yml

lambda_build: lambda_cleanup
	git tag -a $(TAG) -m "Deployed from Makefile"
	git push origin --tags
	mkdir lambda_$(TAG)_deploy
	chmod u=rwx,go=r function.py
	cp -R src lambda_$(TAG)_deploy && cp function.py lambda_$(TAG)_deploy
	pip install -Ur requirements.txt -t ./lambda_$(TAG)_deploy
	rm -rf lambda_$(TAG)_deploy/psycopg2
	mv psycopg2-3.6/ psycopg2/
	cp -R psycopg2 lambda_$(TAG)_deploy/
	mv psycopg2/ psycopg2-3.6/
	cd lambda_$(TAG)_deploy && zip -r -q lambda_$(TAG)_deploy.zip .
	cd ..
	mv lambda_$(TAG)_deploy/lambda_$(TAG)_deploy.zip .

lambda_release: clean lambda_build

lambda_deploy: lambda_release
	aws s3 cp lambda_$(TAG)_deploy.zip s3://tf-redshift-bucket-int-deployments/
	make lambda_cleanup
