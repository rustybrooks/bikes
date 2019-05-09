#!/usr/bin/env bash

cd /srv/src

sleep 2
./bikedb/run.py --migrate

while true; do
    ./bikedb/run.py --sync --continuous=30 
done
