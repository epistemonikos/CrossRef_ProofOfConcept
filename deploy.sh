#!/usr/bin/env bash
echo "Deploying Reference Lookup Service"
# echo "Killing worker..."
# killall rq
git pull
git checkout master
if [ ! -d "./venv" ]; then
    virtualenv --python=python3.5 ./venv
fi
./venv/bin/pip install -r requirements.txt
# echo "Starting worker..."
# screen -d -m ./venv/bin/rq worker
echo "Restarting services..."
sudo service referencelookup restart
sudo service nginx restart
echo "All done!"
