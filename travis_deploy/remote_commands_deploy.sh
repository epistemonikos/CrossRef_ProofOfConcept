#!/usr/bin/env bash

rm -rf /tmp/www_reflookup
cd /tmp
tar xzmfv ./reflookup.tar.gz
mv /tmp/ReferenceLookupService /tmp/www_reflookup
virtualenv --python=python3.5 /tmp/www_reflookup/venv
cd /tmp/www_reflookup
cat ./.env
source ./.env
./venv/bin/pip install -r requirements.txt
killall gunicorn #TODO: FIX
echo "Starting service"
screen -d -m "./venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 reflookup.wsgi:app --error-logfile errors.log & echo $! > ./gunicorn.pid"
killall rq #TODO: FIX TOO
screen -d -m "./venv/bin/rq worker & echo $! > worker.pid"
