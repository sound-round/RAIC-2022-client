#!/bin/bash
rm -rf lastSources.zip
zip -r -X "lastSources.zip" ./codegame/;
zip -r -X "lastSources.zip" ./debugging/;
zip -r -X "lastSources.zip" ./model/;
zip -r -X "lastSources.zip" ./debug_interface.py;
zip -r -X "lastSources.zip" ./main.py;
zip -r -X "lastSources.zip" ./my_strategy.py;
zip -r -X "lastSources.zip" ./stream_wrapper.py;
