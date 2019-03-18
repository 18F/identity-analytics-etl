#!/bin/bash
# -*- coding: utf-8 -*-
#
# Execute Redshift Query.
#
# Usage:
#
#   bash rsq.sh <query-name> <other-psql-options>
#
# Example:
#
#   bash rsq.sh auth_funnel -W -v variable1=value1 -v=variable2=value2
#
# Explain:
#
#   <query-name> is defined in rsq.py file, rsq.py will find the absolute path of a sql file by query name
#   <other-psql-option> can be any psql options other than -h, -p, -d, -U, -W, -f. Usually you use -v var1=value1 -v var2=value2 ... to pass parameters.
#
# This bin tools depends on rsq.py
#
# How to test:
#
#   bash tests/test_rsq.sh # password = 'password'
#
# Expected result:
#
#  count
# -------
#      2

dir_bin="$( cd "$(dirname "$0")" ; pwd -P )"
path_rsq_py="${dir_bin}/rsq.py"


host="$(python $path_rsq_py read_credential host)"
port="$(python $path_rsq_py read_credential port)"
database="$(python $path_rsq_py read_credential database)"
username="$(python $path_rsq_py read_credential username)"

query_name=$1
path_sql="$(python $path_rsq_py get_sql $query_name)"

shift
psql -h $host -p $port -d $database -U $username -f $path_sql "$@"
