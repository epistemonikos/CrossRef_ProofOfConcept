#!/usr/bin/env bash
echo "Deploying Reference Lookup Service\n"
git pull
git checkout master
if [ ! -d "./venv" ]; then
    virtualenv --python=python3.5 ./venv
fi
./venv/bin/pip install -r requirements.txt
echo "Restarting services...\n"
sudo service referencelookup restart
sudo service nginx restart
echo "All done!\n"
