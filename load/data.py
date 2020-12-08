import weaviate.tools
import uuid


def generate_uuid(key):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, key))


class Loader:

    def __init__(self, batcher:weaviate.tools.Batcher):
        self.batcher = batcher
        self.loaded_articles = []

    def load_category(self, data):
        self.batcher.add_data_object(
            data_object=data["schema"],
            class_name=data["class"],
            uuid=data["id"]
        )

    def load_publications(self, data):
        self.batcher.add_data_object(
            data_object=data["schema"],
            class_name=data["class"],
            uuid=data["id"]
        )

    def load_authors_articles(self, data):
        article_id = generate_uuid(data['title'])

        ##### ADD AUTHORS #####
        author_ids = []
        for author in data['authors']:
            author_id = self.add_authors(author, article_id, data['publicationId'])
            if author_id is not None:
                author_ids.append(author_id)
            else:
                # TODO Why to use the publication ID if the author ID is not generated???
                author_ids.append(data['publicationId'])

        ##### ADD ARTICLES #####
        if article_id not in self.loaded_articles:
            self.loaded_articles.append(article_id)
            word_count = len(' '.join(data['paragraphs']).split(' '))
            article_object = {
                'title': data['title'],
                'summary': process_input('Summary', data['summary']),
                'wordCount': word_count,
                'url': data['url'],
            }
            # Set publication date
            if data['pubDate'] is not None and data['pubDate'] != '':
                article_object['publicationDate'] = data['pubDate']
            # Add article to weaviate
            self.batcher.add_data_object(article_object, "Article", article_id)
            # Add reference to weaviate
            self.batcher.add_reference(
                from_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                from_thing_class_name="Article",
                from_thing_uuid=article_id,
                from_property_name="inPublication",
                to_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                to_thing_uuid=data['publicationId'],
            )
            self.batcher.add_reference(
                from_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                from_thing_class_name="Publication",
                from_thing_uuid=data['publicationId'],
                from_property_name="hasArticles",
                to_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                to_thing_uuid=article_id
            )
            self.add_ref_article_authors(author_ids, article_id)

    def add_ref_article_authors(self, author_ids, article_id):
        for author_id in author_ids:
            self.batcher.add_reference(
                from_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                from_thing_class_name="Article",
                from_thing_uuid=article_id,
                from_property_name="hasAuthors",
                to_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                to_thing_uuid=author_id,
            )

    def add_authors(self, author, article_id, publication_id):
        author = process_input('Author', author)
        if len(author.split(' ')) == 2:
            author_uuid = generate_uuid(author)
            self.batcher.add_data_object(
                data_object={'name': author},
                class_name='Author',
                uuid=author_uuid,
            )
            self.batcher.add_reference(
                from_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                from_thing_class_name="Author",
                from_thing_uuid=author_uuid,
                from_property_name="writesFor",
                to_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                to_thing_uuid=publication_id
            )
            self.batcher.add_reference(
                from_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                from_thing_class_name="Author",
                from_thing_uuid=author_uuid,
                from_property_name="wroteArticles",
                to_semantic_type=weaviate.SEMANTIC_TYPE_THINGS,
                to_thing_uuid=article_id
            )
            return generate_uuid(author)
        return None


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