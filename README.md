buildbuild
==========

[![Build Status](https://travis-ci.org/buildbuild/buildbuild.svg?branch=master)](https://travis-ci.org/buildbuild/buildbuild)

Deployment
---
#### Building Container Image
1 .Pulling `buildbuild/buildbuild` image from docker hub :
```
$ sudo docker pull buildbuild/buildbuild
```

2 .Use this `Dockerfile` to build a new image :
```
$ sudo docker build -t buildbuild/buildbuild .
```

#### Running the Container :
```
$ sudo docker run -d -p :8000 buildbuild/buildbuild
```

Managing Static Files
---
1. Install all dependent packages
```
$ python manage.py bower install
```

2. Collect all static files from each of our applications :
```
$ python manage.py collectstatic --noinput
```
it makes every static files copied to STATIC_ROOT folder ( `/static` )

Project Initializing
---
1. $ python migrating.py
2. $ python loadfixtures.py
