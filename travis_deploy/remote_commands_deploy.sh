#!/usr/bin/env bash

rm -rf /tmp/www_reflookup
mkdir /tmp/www_reflookup
virtualenv --python=python3.5 /tmp/www_reflookup/venv
cd /tmp
tar xzmfv /tmp/reflookup.tar.gz
cp -r /tmp/ReferenceLookupService/* /tmp/www_reflookup/
rm -rf /tmp/ReferenceLookupService /tmp/reflookup.tar.gz
cd /tmp/www_reflookup
source ./travis_deploy/.env
./venv/bin/pip install -r requirements.txt
killall gunicorn #TODO: FIX
screen -d -m ./venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 reflookup.wsgi:app --error-logfile errors.log
killall rq #TODO: FIX TOO
screen -d -m ./venv/bin/rq worker
