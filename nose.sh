#!/bin/sh
if [ "$PWD" != "/kata/sources" ]; then
    echo "You are running the script from the wrong directory. Please run it from /kata/sources"
    exit
fi
nosetests --ckan --with-pylons=ckanext-showcase/test-core.ini ckanext-showcase/ckanext/showcase/tests --logging-clear-handlers --logging-filter=ckanext