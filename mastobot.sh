#!/bin/bash

# This script makes heavy use of default parameters
# for the invoked Python scripts. If your needs
# differ, either manually invoke the Python scripts
# or modify this file.

python download.py -k "zelda screenshots"
python mbot.py \
    -k $CLIENT_KEY \
    -s $CLIENT_SECRET \
    -t $ACCESS_TOKEN