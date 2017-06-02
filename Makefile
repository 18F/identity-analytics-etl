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

deploy:
	./deploy
