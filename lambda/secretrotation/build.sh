#! /bin/bash
docker build -t password_rotation . --rm
docker run -d password_rotation
CONTAINER_ID=$(docker ps -alq)
docker cp $CONTAINER_ID:/build/redshift_password_rotation.zip .
docker stop $CONTAINER_ID