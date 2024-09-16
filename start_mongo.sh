#!/bin/bash

# Navigate to the script's directory (in case it's run from elsewhere)
cd "$(dirname "$0")"

# Start mongod with the custom configuration file
mongod --config ./mongodb/mongod.conf