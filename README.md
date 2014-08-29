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

#### Running the Container
```
$ sudo docker run -d -p :8000 buildbuild/buildbuild
```
