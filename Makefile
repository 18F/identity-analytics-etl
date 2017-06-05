venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate

test: venv
	venv/bin/python tests/test.py

destroy_db:
	venv/bin/python src/destroy_db.py

clean: venv destroy_db test
	rm -rf venv

run: venv
	venv/bin/python src/uploader.py

lambda_cleanup:
	rm -f lambda_deploy.zip
	rm -rf lambda_deploy/

lambda_build: lambda_cleanup
	mkdir lambda_deploy
	cp -R src lambda_deploy && cp function.py lambda_deploy
	pip install -Ur requirements.txt -t ./lambda_deploy/
	zip -r lambda_deploy.zip lambda_deploy

lambda_release: clean lambda_build

lambda_deploy: lambda_release
	aws s3 cp lambda_deploy.zip s3://tf-redshift-bucket-$(ENVIRONMENT)-deployments/
	make lambda_cleanup
