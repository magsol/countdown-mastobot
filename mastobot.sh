#!/bin/bash

# This script makes heavy use of default parameters
# for the invoked Python scripts. If your needs
# differ, either manually invoke the Python scripts
# or modify this file.

# Fill in the missing values and uncomment the following three
# lines if you're running this script directly.
#export CLIENT_KEY=your_client_key
#export CLIENT_SECRET=your_client_secret
#export ACCESS_TOKEN=your_access_token

python download.py -k "zelda totk screenshots" -n 40
python mbot.py \
    -k $CLIENT_KEY \
    -s $CLIENT_SECRET \
    -t $ACCESS_TOKEN