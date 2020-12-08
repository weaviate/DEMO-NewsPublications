#!/usr/bin/env python3
# Import necessary libraries
# buildin
import os
import sys
import json
import uuid
from time import sleep
# installed
import weaviate
from weaviate.tools import Batcher
from weaviate import SEMANTIC_TYPE_THINGS


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

    batcher = Batcher(
        client=client, 
        batch_size=batch_size,
    )
    
    if not data_dir.endswith("-nl"):
        ##### ADD CATEGORIES #####
        for filename in os.listdir(data_dir + '/categories'):
            # Use only JSON file formats.
            if filename.endswith(".json"): 
                with open(data_dir + '/categories/' + filename) as file_:
                    object_data = json.load(file_)
                    batcher.add_data_object(
                        data_object=object_data["schema"],
                        class_name=object_data["class"],
                        uuid=object_data["id"]
                    )   
    ##### ADD PUBLICATIONS #####
    for filename in os.listdir(data_dir + '/publications'):
        # Use only JSON file formats.
        if filename.endswith(".json"): 
            with open(data_dir + '/publications/' + filename) as file_:
                object_data = json.load(file_)
                batcher.add_data_object(
                        data_object=object_data["schema"],
                        class_name=object_data["class"],
                        uuid=object_data["id"]
                    )
    batcher.update_batches()
    sleep(3)
    validator = []

    for filename in os.listdir(data_dir):
        # Use only JSON file formats.
        if filename.endswith(".json"): 
            file_ = open(data_dir + '/' + filename)
            object_data = json.load(file_)
            article_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, object_data['title']))

            ##### ADD AUTHORS #####
            authors = add_authors_and_article_ref(
                object_data=object_data,
                article_id=article_id,
                batcher=batcher
            )
            ##### ADD ARTICLES #####
            validator = add_articles_and_publication_ref(
                object_data=object_data,
                article_id=article_id,
                batcher=batcher,
                authors=authors,
                validator=validator
            )
            file_.close()
    batcher.close()
         

def add_authors_and_article_ref(
        object_data: dict,
        article_id: str,
        batcher: Batcher
    ) -> list:
    """
    Add authors and the respective reference to the article they wrote to weaviate.

    Parameters
    ----------
    object_data: dict
        Data of an article represented as a dictionary that contains the authors to add.
    article_id: str
        ID of the article that authors (that need to be added) wrote.
    batcher: Batcher
        A batcher object used to send data to weaviate in batches.

    Returns
    -------
    list
        Returns a list of processed authors names.
    """

    authors = []
    for author in object_data['authors']:
        # check if relation should be through author or publication
        author = process_input('Author', author)
        if len(author.split(' ')) == 2:
            author_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, author))
            batcher.add_data_object(
                data_object=create_author_object(author, object_data['publicationId']),
                class_name='Author',
                uuid=author_uuid,
            )
            batcher.add_reference(
                from_semantic_type=SEMANTIC_TYPE_THINGS,
                from_thing_class_name="Author",
                from_thing_uuid=author_uuid,
                from_property_name="wroteArticles",
                to_semantic_type=SEMANTIC_TYPE_THINGS,
                to_thing_uuid=article_id
            )
            authors.append({
                'beacon': 'weaviate://localhost/things/' + \
                    str(uuid.uuid3(uuid.NAMESPACE_DNS, author))
            })
        else:
            authors.append({
                'beacon': 'weaviate://localhost/things/' + object_data['publicationId']
            })
    return authors

def add_articles_and_publication_ref(
        object_data: dict,
        article_id: str,
        batcher: Batcher,
        authors: list,
        validator: list
    ) -> list:
    """
    Add authors and the respective reference to the article they wrote to weaviate.

    Parameters
    ----------
    object_data: dict
        Data of an article represented as a dictionary that contains the authors to add.
    article_id: str
        ID of the article that authors (that need to be added) wrote.
    batcher: Batcher
        A batcher object used to send data to weaviate in batches.
    authors:
        Authors of the article.
    validator: list
        A list of article ID that has been aready added to weaviate.

    Returns
    -------
    list
        Returns an updated validator list.
    """

    if article_id not in validator:
        validator.append(article_id)
        word_count = len(' '.join(object_data['paragraphs']).split(' '))
        article_object = create_article_object(
            object_data=object_data,
            authors=authors,
            word_count=word_count
        )
        # Set publication date
        if object_data['pubDate'] is not None and object_data['pubDate'] != '':
            article_object['publicationDate'] = object_data['pubDate']
        # Add article to weaviate
        batcher.add_data_object(article_object, "Article", article_id)
        # Add reference to weaviate
        batcher.add_reference(
            from_semantic_type=SEMANTIC_TYPE_THINGS,
            from_thing_class_name="Publication",
            from_thing_uuid=object_data['publicationId'],
            from_property_name="hasArticles",
            to_semantic_type=SEMANTIC_TYPE_THINGS,
            to_thing_uuid=article_id
        )
    return validator

def create_author_object(
        author: str,
        publication_id: str,
    ) -> dict:
    """
    Create author object, as a dictionary, to upload to weaviate.

    Parameters
    ----------
    author: str
        Author name.
    publication_id: str
        Publication ID that the author wrote.

    Returns
    -------
    dict
        Dictionary object to upload to weaviate.
    """


    return {
        'name': author,
        'writesFor': [
            {
                'beacon': 'weaviate://localhost/things/' + publication_id
            }
        ]
    }


def create_article_object(
        object_data: dict,
        authors: list,
        word_count: int
    ) -> dict:
    """
    Create article object, as a dictionary, to upload to weaviate.

    Parameters
    ----------
    object_data: dict
        A dictionary containing all the information about the article.
    authors: list
        A list of authors that wrote this article.
    word_count: int
        How many words are in the article.

    Returns
    -------
    dict
        Dictionary object to upload to weaviate.
    """


    return {
        'title': object_data['title'],
        'summary': process_input('Summary', object_data['summary']),
        'hasAuthors': authors,
        'wordCount': word_count,
        'url': object_data['url'],
        'inPublication': [
            {
                'beacon': 'weaviate://localhost/things/' + object_data['publicationId']
            }
        ]
    }


def process_input(
        class_name: str,
        value: str,
    ) -> str:
    """
    Clean up the data.

    Parameters
    ----------
    class_name: str
        Which class the object(see value) to clean belongs to.
    value: str
        The object to clean.

    Returns
    -------
    str
        Cleaned object.
    """


    if class_name == 'Author':
        value = value.replace(' Wsj.Com', '')
        value = value.replace('.', ' ')
    elif class_name == 'Summary':
        value = value.replace('\n', ' ')
    return value


if __name__ == "__main__":

    print(f"Importing data from: {sys.argv[2]}")
    if len(sys.argv) == 4:
        upload_data_to_weaviate(
            client=weaviate.Client(sys.argv[1]),
            data_dir=sys.argv[2],
            batch_size=int(sys.argv[3])
        )
    else:
        upload_data_to_weaviate(
            client=weaviate.Client(sys.argv[1]),
            data_dir=sys.argv[2],
            batch_size=200
        )
