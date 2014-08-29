FROM ubuntu:precise
MAINTAINER dobestan "dobestan@gmail.com"

# Installing Depenent Packages
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python-dev python-setuptools
RUN apt-get install -y supervisor
RUN apt-get install -y git-core
RUN apt-get install -y libncurses5-dev # included for installing gnureadline installation

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

# in real deployment,
# static files should be collected via manage.py collectstatic command
#
# at this moment, buildbuild django project has no static files
# so collectstatic command is intentionally excluded from Dockerfile
#
# before uncomment below RUN command,
# should explicitly set STATIC_ROOT in buildbuild/settings.py
#
# for example,
# RUN (cd /opt/apps/buildbuild && /opt/ve/buildbuild/bin/python manage.py collectstatic --noinput)

EXPOSE 8000
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]
