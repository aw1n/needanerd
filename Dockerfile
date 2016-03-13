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
CMD rm -fr /var/cache/yum/*
RUN yum clean all

# Update sources
RUN yum -y install epel-release; yum clean all
RUN yum -y install python-pip; yum clean all
RUN yum -y install python-django; yum clean all
RUN yum -y install python-devel; yum clean all
RUN yum -y install git; yum clean all
RUN yum -y install sqlite; yum clean all
RUN yum -y install gcc make; yum clean all
RUN yum -y install libxslt-devel; yum clean all
RUN yum -y install libxml2-devel; yum clean all
RUN yum -y install libxml2; yum clean all
RUN yum -y install libxslt; yum clean all
RUN yum -y install python-lxml; yum clean all
RUN yum -y install python-openid; yum clean all
RUN yum -y install python-requests-oauthlib; yum clean all
RUN yum -y install postgresql; yum clean all
RUN yum -y install postgresql-contrib; yum clean all
RUN yum -y install postgresql-devel; yum clean all
RUN yum -y install bind-utils; yum clean all

# Build tools so that we can build Python from source
#RUN yum -y group install 'Development Tools'
#RUN yum -y install tar

RUN pip install lxml==3.4.4
RUN pip install psycopg2==2.6.1
RUN pip install django=="$DJANGO_VERSION"
RUN pip install python-social-auth==0.2.14

#This cache bust makes sure the docker build gets the latest code from github
ARG CACHEBUST=1
RUN git clone https://github.com/johnfosborneiii/needanerd 

# Port to expose
EXPOSE 8888

CMD python2.7 needanerd/manage.py runserver 0.0.0.0:8888

