#!/bin/bash
set -e

# Download adblock lists
mkdir -p feature_extraction/adblock
wget https://easylist.to/easylist/easylist.txt -P adblock
wget https://easylist.to/easylist/easyprivacy.txt -P adblock
wget https://github.com/disconnectme/disconnect-tracking-protection/blob/master/services.json  -O adblock/disconnect.json
sudo pip install adblockparser
