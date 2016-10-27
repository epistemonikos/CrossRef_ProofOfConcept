#!/usr/bin/env bash
eval "$(ssh-agent -s)" #start the ssh agent
chmod 600 travis_deploy/travis_ci.rsa # this key should have push access
ssh-add travis_deploy/travis_ci.rsa
invoke deploy
