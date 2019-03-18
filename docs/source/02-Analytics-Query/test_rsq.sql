/*
This is for testing ./bin/rsq.sh only
*/
SELECT COUNT(*)
FROM test_rsq_users T
WHERE T.id <= :upper;
