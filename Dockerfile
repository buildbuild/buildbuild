FROM ubuntu:trusty
MAINTAINER dobestan "dobestan@gmail.com"

# Installing Depenent Packages
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev python-setuptools
RUN apt-get install -y supervisor
RUN apt-get install -y git-core
RUN apt-get install -y libncurses5-dev # included for installing gnureadline installation
RUN apt-get install -y nodejs
RUN apt-get install -y nodejs-legacy
RUN apt-get install -y npm

RUN npm install -g bower

# Installing Python Pacakges
RUN easy_install pip
RUN pip install virtualenv
RUN pip install uwsgi

# Where everything goes ...
#   /opt/ve/buildbuild : virtualenv python enviroment
#   /opt/apps/buildbuild : django apps
#   /opt/ : configuration settings ( in this case, supervisor.conf )
#   /usr/local/bin/ : custom script ( in this case, run script : simple script running supervisord via supervisor.conf )

RUN virtualenv --no-site-packages /opt/ve/buildbuild

ADD . /opt/apps/buildbuild

ADD .docker/supervisor.conf /opt/supervisor.conf
ADD .docker/run.sh /usr/local/bin/run

RUN /opt/ve/buildbuild/bin/pip install -r /opt/apps/buildbuild/requirements.txt

RUN (cd /opt/apps/buildbuild/buildbuild && /opt/ve/buildbuild/bin/python manage.py syncdb --noinput)

RUN (cd /opt/apps/buildbuild/buildbuild && /opt/ve/buildbuild/bin/python manage.py bower install)
RUN (cd /opt/apps/buildbuild/buildbuild && /opt/ve/buildbuild/bin/python manage.py collectstatic --noinput)

EXPOSE 8000
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]
