# Newspapers and Magazine // Weaviate

This demo shows how Weaviate can be used to explore magazines and newspapers.

_ARTICLES ARE USED FOR DEMO PURPOSES ONLY!_

_IF YOU WANT TO USE THIS DEMO, JUST RUN THE DOCKER FROM THE DOCS http://127.0.0.1:4000/documentation/weaviate/current/index.html_

## Installation (for collecting data) (ENGLISH)

Make sure to have Python3 and pip3 installed.

If you don't have NLTK installed

1. `$ ./downloadNltk.py`

Only if you want to start with a fresh dataset (the cache folder is populated);

1. `$ rm ./cache/*`
2. `$ ./download.py ft & ./download.py nyt & ./download.py guardian & ./download.py wsj & ./download.py cnn & ./download.py fn & ./download.py econ & ./download.py newyorker & ./download.py wired & ./download.py vogue & ./download.py gi &`

Execute the import

1. `$ pip3 install weaviate-cli`
2. `$ pip3 install -r requirements.txt`
3. `$ echo '{"url": "<WEAVIATE URL>", "auth": null}' > ./config.json`
4. `$ weaviate-cli --config-file ./config.json schema import ./schema.json --force`
5. `$ ./import-nl.py <WEAVIATE URL> './cache'`

## Create Docker

1. `$ docker build . --tag="semitechnologies/weaviate-demo-newspublications:latest" --no-cache`
2. `$ docker push semitechnologies/weaviate-demo-newspublications:latest`

## Import data without Docker

0. Clone this repo.
0. `$ pip3 install -r requirements.txt`
0. `$ pip3 install weaviate-cli`
0. Run `./import.sh {URL TO YOUR WEAVIATE}` e.g., `./import.sh http://localhost:8080`

## Installation (for collecting data) (DUTCH)

For Dutch newspapers, do the following:

Make sure to have Python3 and pip3 installed.

If you don't have NLTK installed

1. `$ ./downloadNltk.py`

Only if you want to start with a fresh dataset (the cache folder is populated);

1. `$ rm ./cache/*`
2. `$ /download-nl.py dvhn & ./download.py nos & ./download.py nu & ./download.py ad & ./download.py nrc & ./download.py telegraaf & ./download.py fd & ./download.py volkskrant & ./download.py trouw & ./download.py rtl & ./download.py elsevier & ./download.py parool & ./download.py gelderlander & ./download.py tweakers & ./download.py metro &`

Execute the import

1. `$ pip3 install weaviate-cli`
2. `$ pip3 install -r requirements.txt`
3. `$ echo '{"url": "<WEAVIATE URL>", "auth": null}' > ./config.json`
4. `$ weaviate-cli --config-file ./config.json schema import ./schema.json --force`
5. `$ ./import-nl.py <WEAVIATE URL> './cache-nl'`

## Create Docker

1. `$ docker build . --tag="semitechnologies/weaviate-demo-newspublications-nl:latest" --no-cache`
2. `$ docker push semitechnologies/weaviate-demo-newspublications-nl:latest`

## Import data without Docker

0. Clone this repo.
0. `$ pip3 install -r requirements.txt`
0. `$ pip3 install weaviate-cli`
0. Run `./import.sh {URL TO YOUR WEAVIATE}` e.g., `./import.sh http://localhost:8080`

