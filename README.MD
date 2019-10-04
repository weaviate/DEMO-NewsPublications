# Newspapers and Magazine // Weaviate

This demo shows how Weaviate can be used to explore magazines and newspapers

## Installation

Make sure to have Python3 and pip3 installed.

1. [Install weaviate-cli](https://www.semi.technology/documentation/weaviate-cli/current/installation.html).
2. `$ pip3 install -r requirements.txt`
3. `$ weaviate-cli cluster-create`
4. `$ weaviate-cli schema-import --location=schema.json`
5. `$ ./download.py ft & ./download.py nyt & ./download.py guardian & ./download.py wsj & ./download.py cnn & ./download.py fn & ./download.py econ & ./download.py newyorker & ./download.py wired & ./download.py vogue & ./download.py gi`
6. `$ ./import.py`