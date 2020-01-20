# Newspapers and Magazine // Weaviate

This demo shows how Weaviate can be used to explore magazines and newspapers.

_ARTICLES ARE USED FOR DEMO PURPOSES ONLY!_

_IF YOU WANT TO USE THIS DEMO, JUST RUN THE DOCKER FROM THE DOCS http://127.0.0.1:4000/documentation/weaviate/current/index.html_

## Installation (for collecting data)

Make sure to have Python3 and pip3 installed.

If you don't have NLTK installed

1. `$ ./downloadNltk.py`

Only if you want to start with a fresh dataset (the cache folder is populated);

1. `$ rm ./cache/*`
2. `$ ./download.py ft & ./download.py nyt & ./download.py guardian & ./download.py wsj & ./download.py cnn & ./download.py fn & ./download.py econ & ./download.py newyorker & ./download.py wired & ./download.py vogue & ./download.py gi &`

Execute the import

1. [Install weaviate-cli](https://www.semi.technology/documentation/weaviate-cli/current/installation.html).
2. `$ pip3 install -r requirements.txt`
3. `$ weaviate-cli cluster-create`
4. `$ weaviate-cli schema-import --location=schema.json`
5. `$ ./import.py`

## Create Docker

1. `$ docker build . --tag="semitechnologies/weaviate-demo-newspublications:latest" --no-cache`
2. `$ docker push semitechnologies/weaviate-demo-newspublications:latest`

## Import data without Docker

0. Clone this repo.
0. `$ pip3 install -r requirements.txt`
0. [Install weaviate-cli](https://www.semi.technology/documentation/weaviate-cli/current/installation.html).
0. Run `./import.sh {URL TO YOUR WEAVIATE}` e.g., `./import.sh http://localhost:8080`
