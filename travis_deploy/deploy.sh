#!/usr/bin/env bash
if [ "$TRAVIS_BRANCH" = "master" ]; then
    echo "Starting deploy."
    echo "Packing distribution package..."
    cd ..
    DIST="/tmp/reflookup.tar.gz"
    tar czfv "$DIST" --exclude-vcs --exclude='.idea' --exclude='venv' --exclude="__pycache__" ReferenceLookupService
    cd ReferenceLookupService
    echo "Pushing to remote..."
    scp -o StrictHostKeyChecking=no "$DIST" "ubuntu@52.3.221.80:$DIST"
    cat travis_deploy/remote_commands_deploy.sh|ssh -o StrictHostKeyChecking=no ubuntu@52.3.221.80
    echo "Done"
fi
