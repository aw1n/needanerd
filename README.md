# needanerd

Source code is available here: https://github.com/johnfosborneiii/needanerd

To run the Docker Container
docker run -d --name postgresql_database -e POSTGRESQL_USER=nerd -e POSTGRESQL_PASSWORD=AuburnUniversity2016! -e POSTGRESQL_DATABASE=nan_db -p 5432:5432 centos/postgresql-94-centos7

If you want to use persistent storage, setup a data container (best practice)
https://docs.docker.com/v1.8/userguide/dockervolumes/

docker create -v /data --name dbdata centos:centos7 /bin/true
docker run -d --volumes-from dbdata --name nan-postgres -p 5432:5432  -e POSTGRESQL_USER=nerd -e POSTGRESQL_PASSWORD=AuburnUniversity2016! -e POSTGRESQL_DATABASE=nan_db  centos/postgresql-94-centos7

FYI you can clean up images with:
docker ps -a | grep 'weeks ago' | awk '{print $1}' | xargs --no-run-if-empty docker rm
OR
docker rm `docker ps -aq`

Build and run in a docker container
cd dockerfiles/
docker build --tag=needanerd-web .
docker run -it -p 8888:8888 needanerd-web
docker run -it --link nan-postgres -p 8888:8888 needanerd-web

Verify the connection with:
export PGPASSWORD='AuburnUniversity2016!'; psql -h localhost -p 5432 -U nerd -w nan_db

