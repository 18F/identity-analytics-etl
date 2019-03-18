#!/bin/bash
#
# Use postgres image on https://hub.docker.com/_/postgres for tests
#
# 1. run container
# 2. create dummy credential file, test db, test table, data
# 3. test ./bin/rsq.sh
# 4. stop container

dir_tests="$( cd "$(dirname "$0")" ; pwd -P )"
dir_project_root="$(dirname "${dir_tests}")"
path_rsq_sh="${dir_project_root}/bin/rsq.sh"
path_test_rst_py="${dir_tests}/test_rsq.py"

docker run --rm --name identity-analytics-etl-test -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres
python $path_test_rst_py
bash $path_rsq_sh test_rsq -w password -v upper=2
docker container stop identity-analytics-etl-test