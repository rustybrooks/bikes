#!/usr/bin/env bash

cd /srv/src

sleep 15
./bikedb/run.py --migrate

while true; do
    ./bikedb/run.py --sync --continuous=300
    sleep 10
done
