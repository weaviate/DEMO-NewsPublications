#!/usr/bin/env python3
# Import necessary libraries
# buildin
import os
import sys
import json
# installed
import weaviate
from weaviate.tools import Batcher
import time
from load.data import Loader


def batcher_callback(results):
    for r in results:
        result = r['result']
        if result.get('status', 'SUCCESS') != 'SUCCESS':
            print(r)
        if 'error' in result:
            print(r)


def iterate_json(path: str, callback):
    for filename in os.listdir(path):
        # Use only JSON file formats.
        if filename.endswith(".json"):
            file_path = os.path.join(path, filename)
            with open(file_path) as file:
                data = json.load(file)
                callback(data)


def upload_data_to_weaviate(
        client: weaviate.Client,
        data_dir: str,
        batch_size:int = 200
    ) -> None:
    """
    Upload data to weaviate.

    Parameters
    ----------
    client: weaviate.Client
        Weaviate client.
    data_dir: str
        Directory with the data files to read in.
    batch_size:int = 200
        Number of objects to upload at once to weaviate.

    Returns
    -------
    None
    """

    with Batcher(
        client=client, 
        batch_size=batch_size,
        return_values_callback=batcher_callback
    ) as batcher:
        loader = Loader(batcher)

        if not data_dir.endswith("-nl"):
            ##### ADD CATEGORIES #####
            iterate_json(data_dir + '/categories', loader.load_category)

        ##### ADD PUBLICATIONS #####
        iterate_json(data_dir + '/publications', loader.load_publications)

        iterate_json(data_dir, loader.load_authors_articles)
         

if __name__ == "__main__":
    client = weaviate.Client(sys.argv[1])
    while not client.is_ready():
        print("wait for weaviate to get ready.")
        time.sleep(2.0)
    if not client.schema.contains():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        schema_file = os.path.join(dir_path, "schema.json")
        client.schema.create(schema_file)

    print(f"Importing data from: {sys.argv[2]}")
    if len(sys.argv) == 4:
        upload_data_to_weaviate(
            client=client,
            data_dir=sys.argv[2],
            batch_size=int(sys.argv[3])
        )
    else:
        upload_data_to_weaviate(
            client=client,
            data_dir=sys.argv[2],
            batch_size=200
        )
