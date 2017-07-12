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

lambda_build: lambda_cleanup
	git tag -a $(TAG) -m "Deployed from Makefile"
	git push origin --tags
	mkdir lambda_$(TAG)_deploy
	cp -R src lambda_$(TAG)_deploy && cp function.py lambda_$(TAG)_deploy
	pip install -Ur requirements.txt -t ./lambda_$(TAG)_deploy/
	zip -r lambda_$(TAG)_deploy.zip lambda_$(TAG)_deploy

lambda_release: clean lambda_build

lambda_deploy: lambda_release
	aws s3 cp lambda_$(TAG)_deploy.zip s3://tf-redshift-bucket-$(ENVIRONMENT)-deployments/
	make lambda_cleanup
