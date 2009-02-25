#!/bin/sh

BASE_URL='http://planeta.python.org.ar/'

if [ ! -d feedvalidator ]
then
	svn checkout http://feedvalidator.googlecode.com/svn/trunk/feedvalidator
    cd feedvalidator || exit 1
else
    cd feedvalidator
    svn update
fi 

python src/demo.py $BASE_URL'index.xml'
python src/demo.py $BASE_URL'python.xml'