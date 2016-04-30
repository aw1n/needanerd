# needanerd

Notes:
- SSL is always required. This is a best practice as followed by most social networkig sites.  Performance is degredaded slightly however with the requirement.
- Django admin interface is still active, which is not a best practice and should be at least limited by IP or protected by other security measures
- DEBUG = True. Before going to production turn DEBUG to OFF for performance and security reasons: https://docs.djangoproject.com/en/1.9/howto/error-reporting/

Source code is available here: https://github.com/johnfosborneiii/needanerd

To run the Docker Container
#docker run -d --name needanerd-db -e POSTGRESQL_USER=nerd -e POSTGRESQL_PASSWORD=AuburnUniversity2016! -e POSTGRESQL_DATABASE=nan_db -p 5432:5432 centos/postgresql-94-centos7
docker run -d --name needanerd-db -e POSTGRESQL_USER=nerd -e POSTGRESQL_PASSWORD=AuburnUniversity2016! -e POSTGRESQL_DATABASE=nan_db -p 5432:5432 johnfosborneiii/needanerd-db

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
docker build --tag=johnfosborneiii/needanerd-web .
#docker run -it -p 8888:8888 needanerd-web
docker run -it -d --name needanerd-web --link needanerd-db -p 8888:8888 johnfosborneiii/needanerd-web (if not using a container for storage)

Verify the connection with:
export PGPASSWORD='AuburnUniversity2016!'; psql -h localhost -p 5432 -U nerd -w nan_db

To setup with OpenShift
1. Install the database:
oc new-app --docker-image=centos/postgresql-94-centos7 -e POSTGRESQL_USER=nerd -e POSTGRESQL_PASSWORD=AuburnUniversity2016! -e POSTGRESQL_DATABASE=nan_db --labels='name=nandb'

2. Install Need A Nerd
oc new-app johnfosborneiii/needanerd-web -e ON_OPENSHIFT=TRUE --labels='name=needanerd'

3. From the terminal of the need a nerd container go to the /needanerd/ directory and run
python manage.py migrate

Beware of pushing to docker hub, you may need to change the ~/.docker/config.json file:
https://forums.docker.com/t/docker-push-not-working-in-1-8-1-not-logged-in/2894/19

Build and run from the Dockerfile:
docker build -t johnfosborneiii/needanerd-web --no-cache .
docker push johnfosborneiii/needanerd-web


