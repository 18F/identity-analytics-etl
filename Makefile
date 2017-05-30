init:
	pip install -r requirements.txt

test: init
				python tests/test.py

destroy_db:
	python src/destroy_db.py

clean_install: init destroy_db test

run: init
			python src/uploader.py
