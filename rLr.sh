#!/bin/bash
./kill.sh || true && echo 'startLr' && cd ./lr && ./aicup22 --config ./config.json &

sleep 2;