#!/bin/bash

# when using with Docker compose we need to sleep
echo "Wait for server to come live"
while [ "$RESPONSE" != "200" ]; do
    RESPONSE=$(curl --write-out %{http_code} --silent --output /dev/null $1/v1/meta)
    echo $RESPONSE
    sleep 3
done

# Inform
echo "Importing $1"

# make weaviate cli config file
echo '{"url": "'$1'", "auth": null}' > ./config.json

# import the schema
weaviate-cli --config-file ./config.json schema import ./schema.json --force

# import into Weaviate
./import.py $1 './cache'
