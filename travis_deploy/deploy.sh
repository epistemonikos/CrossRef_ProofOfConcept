#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" = "master" ]; then
    echo "Starting deploy on server."
    invoke deploy
fi
