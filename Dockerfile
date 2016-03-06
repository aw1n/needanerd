############################################################
# Dockerfile to run a Django-based web application
# Based on a CentOS Image
############################################################

# Set the base image to use to Ubuntu
FROM centos:centos7
MAINTAINER John Osborne <johnfosborneiii@gmail.com>

ENV DJANGO_VERSION 1.9.2

# Update sources
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all
RUN yum -y install python-django python-devel git sqlite; yum clean all
RUN yum -y install python-openid python-requests-oauthlib; yum clean all
RUN yum -y install gcc make; yum clean all
RUN yum -y install libxslt-devel libxml2-devel libxml2 libxslt python-lxml; yum clean all

RUN yum -y install postgresql postgresql-contrib postgresql-devel; yum clean all

# Build tools so that we can build Python from source
RUN yum -y group install 'Development Tools'
RUN yum -y install tar

RUN pip install lxml==3.4.4
RUN pip install psycopg2 ==2.6.1
RUN pip install django=="$DJANGO_VERSION"
RUN pip install python-social-auth==0.2.14

ARG CACHEBUST=1 #This cache bust makes sure the docker build gets the latest code from github
RUN git clone https://github.com/johnfosborneiii/needanerd 

# Port to expose
EXPOSE 8888

CMD python2.7 needanerd/manage.py runserver 0.0.0.0:8888

# Install Cookiecutter
# RUN pip install --no-cache-dir cookiecutter
# Generate a Django project from cookiecutter-django
# RUN cookiecutter https://github.com/johnfosborneiii/needanerd --no-input

