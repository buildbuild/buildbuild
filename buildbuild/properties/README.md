### This app provides initial data for Available Project language, version, and docker text ###

* If you want to know that a language is available, use
```
[ AvailableLanguage.objects.get(<language>) ]
```
* If you want to know that a language and version is available, use
```
[ VersionList.objects.get(lang=<language>, ver=<version>) ]
```

### Usage of Django Initial data providing ###

* Print DB data
```
$ ./manage.py dumpdata <app_name> --format=<file extension> > <fixture file path>
```
* Load fixture data & Save into DB
```
$ ./manage.py loaddata.py <fixture file path>
```
