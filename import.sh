#!/bin/bash

# when using with Docker compose we need to sleep
echo "Sleeping to make sure all services are up and running"
sleep 16

# Inform
echo "Importing $1"

# Init the CLI tool
weaviate-cli init --email=noreply@semi.technology --url=$1

# import the schema
weaviate-cli schema-truncate --force
weaviate-cli schema-import --location=/root/DEMO-NewsPublications/schema.json

# import into Weaviate
/root/DEMO-NewsPublications/import.py $1 '/root/DEMO-NewsPublications/cache'
