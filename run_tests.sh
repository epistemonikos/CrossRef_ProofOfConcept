#!/usr/bin/env bash
rq worker &
python test_runner.py
killall rq
