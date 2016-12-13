#!/usr/bin/env bash
# script for remote deploy. It create virtualenv, install requirements and start service
rm -rf /tmp/www_reflookup
cd /tmp
tar xzmfv ./reflookup.tar.gz
mv /tmp/ReferenceLookupService /tmp/www_reflookup
virtualenv --python=python3.5 /tmp/www_reflookup/venv
cd /tmp/www_reflookup
cat ./.env
source ./.env
./venv/bin/pip install -r requirements.txt

if [ -f /tmp/gunicorn.pid ]; then
    kill "$(cat /tmp/gunicorn.pid)"
    rm /tmp/gunicorn.pid
fi
if [ -f /tmp/worker.pid ]; then
    kill "$(cat /tmp/worker.pid)"
    rm /tmp/worker.pid
fi

if [ ! -f /tmp/refservice.db ]; then
    ./venv/bin/python db_manage.py create_db
fi

echo "Starting service"
screen -d -m ./venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 reflookup.wsgi:app --error-logfile errors.log --pid /tmp/gunicorn.pid
screen -d -m ./venv/bin/rq worker --pid /tmp/worker.pid
