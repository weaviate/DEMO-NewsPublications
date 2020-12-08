#!/bin/bash
# Usage: ./import.sh <WEAVIATE_URL> <CACHE_DIR> [BATCH_SIZE]

# when using with Docker compose we need to sleep
echo "Wait for server to come live"
while [ "$RESPONSE" != "200" ]; do
    RESPONSE=$(curl --write-out %{http_code} --silent --output /dev/null $1/v1/meta)
    echo $RESPONSE
    sleep 3
done

# Inform
echo "Importing $1"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# make weaviate cli config file
echo '{"url": "'$1'", "auth": null}' > $DIR/config.json

# import the schema
weaviate-cli --config-file $DIR/config.json schema import $DIR/schema.json

# import into Weaviate
if [[ $# -eq 2 ]]
then
    echo "Import data into weaviate with default batch size (200)"
    $DIR/import.py $1 "$DIR/$2"
elif [[ $# -eq 3 ]]
then
    echo "Import data into weaviate with batch size $3"
    $DIR/import.py $1 "$DIR/$2" $3
else
    echo "ERROR, Wrong number of arguments!"
    exit 1
fi
