#!/bin/bash

# Import the schema
weaviate-cli init --email noreply@semi.technology --url $1

# import into Weaviate
./import.sh $1
