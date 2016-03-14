############################################################
# Dockerfile to run a Django-based web application
# Based on a CentOS Image
############################################################

# Set the base image to use to Ubuntu
#FROM registry.hub.docker.com/centos:centos7
FROM centos:centos7
MAINTAINER John Osborne <johnfosborneiii@gmail.com>

ENV DJANGO_VERSION 1.9.2

#Clear the local client cache
#CMD rm -fr /var/cache/yum/*
#RUN yum clean all

# Update sources
RUN yum -y install epel-release bind-utils; yum clean all
RUN yum -y install git sqlite gcc make; yum clean all
RUN yum -y install python-pip python-django python-devel python-lxml python-openid python-requests-oauthlib; yum clean all
RUN yum -y install libxslt-devel libxml2-devel libxml2 libxslt; yum clean all
RUN yum -y install postgresql postgresql-contrib postgresql-devel; yum clean all

RUN pip install lxml==3.4.4
RUN pip install psycopg2==2.6.1
RUN pip install django=="$DJANGO_VERSION"
RUN pip install python-social-auth==0.2.14
RUN pip install django-bootstrap3

#This cache bust makes sure the docker build gets the latest code from github
ARG CACHEBUST=1
RUN git clone https://github.com/johnfosborneiii/needanerd 

# Port to expose
EXPOSE 8888

CMD python2.7 needanerd/manage.py runserver 0.0.0.0:8888

