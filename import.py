#!/usr/bin/env python3
"""
Import data into weaviate script.
"""
# Import necessary libraries
# buildin
import os
import sys
import json
import time
from typing import Callable
# installed
import weaviate
from weaviate.tools import Batcher
from load.data import Loader


def batcher_callback(
        results: list
    ) -> None:
    """
    Print error message that comes from the batcher update.

    Parameters
    ----------
    results : list
        A list of result for object that were uploaded to weaviate using the batcher.
    """


    for result in results:
        if result['result'].get('status', 'SUCCESS') != 'SUCCESS':
            print(result)
        elif ('errors' in result['result']):
            print(result['errors'])


def iterate_json(
        path: str,
        callback: Callable[[dict], None]
    ) -> None:
    """
    Parse cached files and apply a function to each of them.

    Parameters
    ----------
    path : str
        Cache directory to read files from (only JSON format files supported at the moment).
    callback : Callable[[dict], None]
        The callback function used on each JSON file.
        Ex.: Can be a function that adds to weaviated, or deletes.
    """

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
        iterate_json(data_dir + '/publications', loader.load_publication)

        ##### ADD AUTHORS AND ARTICLES #####
        iterate_json(data_dir, loader.load_authors_article)

def print_usage():
    """
    Print command-line interface description.
    """

    print("Usage: ./import.py <WEAVIATE_URL> <CACHE_DIR> [BATCH_SIZE]")

def main():
    """
    The main function that is executed when running this script.
    """

    nr_argv = len(sys.argv)
    if nr_argv not in (3, 4):
        print(f"ERROR: Too many arguments, given {nr_argv} but must be 3 or 4.")
        print_usage()
        sys.exit(1)

    main_client = weaviate.Client(sys.argv[1])
    wait_time_limit = 14
    while not main_client.is_ready():
        if not wait_time_limit:
            sys.stderr.write("\rTIMEOUT: Weaviate not ready. \
                            Try again or check if weaviate is running.\n")
            sys.exit(1)
        sys.stdout.write(f"\rWait for weaviate to get ready. {wait_time_limit:02d} seconds left.")
        sys.stdout.flush()
        wait_time_limit -= 2
        time.sleep(2.0)

    if not main_client.schema.contains():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        schema_file = os.path.join(dir_path, "schema.json")
        main_client.schema.create(schema_file)

    print(f"\nImporting data from: {sys.argv[2]}")
    if nr_argv == 4:
        upload_data_to_weaviate(
            client=main_client,
            data_dir=sys.argv[2],
            batch_size=int(sys.argv[3])
        )
    else:
        upload_data_to_weaviate(
            client=main_client,
            data_dir=sys.argv[2],
            batch_size=200
        )

if __name__ == "__main__":
    main()
