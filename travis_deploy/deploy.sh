#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" = "master" ]; then
    echo "Starting deploy on server."
    eval "$(ssh-agent -s)" #start the ssh agent
    echo "Adding key to ssh-agent."
    chmod 600 travis_deploy/travis_ci.rsa # this key should have push access
    ssh-add travis_deploy/travis_ci.rsa
    echo "Deploying..."
    invoke deploy
fi
